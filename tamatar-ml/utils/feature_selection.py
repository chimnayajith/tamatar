import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import numpy as np
import pickle

from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.pipeline import Pipeline

from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

# =========================================================
# LOAD DATA
# =========================================================
features_dir = Path(__file__).resolve().parents[1] / "features"
features_path = features_dir / "combined_features.npy"
labels_path   = features_dir / "labels.npy"

X_raw = np.load(str(features_path))
y_raw = np.load(str(labels_path))

label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y_raw)
class_names = list(label_encoder.classes_)

print(f"Loaded features: {X_raw.shape}")
print(f"Loaded labels:   {y.shape}")

n_features = X_raw.shape[1]

# =========================================================
# GAIN RATIO FUNCTIONS
# =========================================================
def entropy(labels):
    classes, counts = np.unique(labels, return_counts=True)
    probs = counts / len(labels)
    return -np.sum(probs * np.log2(probs + 1e-12))

def compute_gain_ratio(feature_col, y):
    unique_vals = np.unique(feature_col)

    if len(unique_vals) < 2:
        return 0

    thresholds = (unique_vals[:-1] + unique_vals[1:]) / 2

    if len(thresholds) > 50:
        thresholds = thresholds[np.linspace(0, len(thresholds)-1, 50, dtype=int)]

    base_entropy = entropy(y)
    best_gr = 0

    for threshold in thresholds:
        left_mask = feature_col <= threshold
        right_mask = feature_col > threshold

        if left_mask.sum() == 0 or right_mask.sum() == 0:
            continue

        n = len(y)

        left_entropy = entropy(y[left_mask])
        right_entropy = entropy(y[right_mask])

        weighted_entropy = (left_mask.sum()/n)*left_entropy + (right_mask.sum()/n)*right_entropy
        info_gain = base_entropy - weighted_entropy

        p_left = left_mask.sum()/n
        p_right = right_mask.sum()/n

        split_info = 0
        if p_left > 0:
            split_info -= p_left * np.log2(p_left)
        if p_right > 0:
            split_info -= p_right * np.log2(p_right)

        if split_info == 0:
            continue

        gr = info_gain / split_info
        best_gr = max(best_gr, gr)

    return best_gr

# =========================================================
# NORMALIZE ONLY FOR GAIN RATIO RANKING PURPOSE
# =========================================================
temp_scaler = StandardScaler()
X_scaled_for_gr = temp_scaler.fit_transform(X_raw)

print("\n" + "="*60)
print("STAGE 1: COMPUTING TRUE GAIN RATIO")
print("="*60)

gr_scores = np.array([compute_gain_ratio(X_scaled_for_gr[:, i], y) for i in range(n_features)])
ranked_indices = np.argsort(gr_scores)[::-1]

for rank, idx in enumerate(ranked_indices):
    print(f"Rank {rank+1:2d} | Feature {idx:2d} | GR = {gr_scores[idx]:.6f}")

# =========================================================
# CLASSIFIERS
# =========================================================
classifiers = {
    "NB": GaussianNB(),
    "LDA": LinearDiscriminantAnalysis(),
    "QDA": QuadraticDiscriminantAnalysis(),
    "LSVM": SVC(kernel='linear'),
    "DT": DecisionTreeClassifier(random_state=42),
    "KNN": KNeighborsClassifier(n_neighbors=3, metric='euclidean')
}

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

output_dir = features_dir
output_dir.mkdir(parents=True, exist_ok=True)
all_results = {}

# =========================================================
# EVALUATION FUNCTION WITH NO DATA LEAKAGE
# =========================================================
def evaluate_subset(model, feature_indices, cache):
    if len(feature_indices) == 0:
        return 0.0

    key = tuple(sorted([int(i) for i in feature_indices]))

    if key in cache:
        return cache[key]

    X_sub = X_raw[:, list(key)]

    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('clf', model)
    ])

    score = cross_val_score(pipeline, X_sub, y, cv=cv, scoring='accuracy', n_jobs=-1).mean()
    cache[key] = score
    return score

# =========================================================
# MAIN LOOP
# =========================================================
for clf_name, classifier in classifiers.items():

    print("\n" + "#"*80)
    print(f"RUNNING HYBRID FEATURE SELECTION FOR {clf_name}")
    print("#"*80)

    evaluation_cache = {}

    # ========================= FORWARD SEARCH =========================
    selected_forward = []
    best_acc_forward = 0

    while True:
        best_candidate_acc = best_acc_forward
        best_feature = None

        for idx in ranked_indices:
            if idx not in selected_forward:
                candidate = selected_forward + [idx]
                acc = evaluate_subset(classifier, candidate, evaluation_cache)

                if acc > best_candidate_acc:
                    best_candidate_acc = acc
                    best_feature = idx

        if best_feature is None:
            break

        selected_forward.append(int(best_feature))
        best_acc_forward = best_candidate_acc
        print(f"[FORWARD ADD] {best_feature:2d} -> {best_acc_forward*100:.4f}%")

    # ========================= BACKWARD SEARCH =========================
    selected_backward = [int(i) for i in ranked_indices]
    best_acc_backward = evaluate_subset(classifier, selected_backward, evaluation_cache)

    while True:
        best_candidate_acc = best_acc_backward
        remove_feature = None

        for idx in selected_backward[::-1]:
            candidate = [f for f in selected_backward if f != idx]
            acc = evaluate_subset(classifier, candidate, evaluation_cache)

            if acc > best_candidate_acc:
                best_candidate_acc = acc
                remove_feature = idx

        if remove_feature is None:
            break

        selected_backward.remove(remove_feature)
        best_acc_backward = best_candidate_acc
        print(f"[BACKWARD REMOVE] {remove_feature:2d} -> {best_acc_backward*100:.4f}%")

    # ========================= BIDIRECTIONAL SEARCH =========================
    selected_bidir = []
    best_acc_bidir = 0

    while True:
        changed = False

        # ADD
        best_candidate_acc = best_acc_bidir
        best_feature = None

        for idx in ranked_indices:
            if idx not in selected_bidir:
                candidate = selected_bidir + [idx]
                acc = evaluate_subset(classifier, candidate, evaluation_cache)

                if acc > best_candidate_acc:
                    best_candidate_acc = acc
                    best_feature = idx

        if best_feature is not None:
            selected_bidir.append(int(best_feature))
            best_acc_bidir = best_candidate_acc
            changed = True
            print(f"[BIDIR ADD] {best_feature:2d} -> {best_acc_bidir*100:.4f}%")

        # REMOVE
        best_candidate_acc = best_acc_bidir
        remove_feature = None

        for idx in selected_bidir:
            candidate = [f for f in selected_bidir if f != idx]
            if len(candidate) == 0:
                continue

            acc = evaluate_subset(classifier, candidate, evaluation_cache)

            if acc > best_candidate_acc:
                best_candidate_acc = acc
                remove_feature = idx

        if remove_feature is not None:
            selected_bidir.remove(remove_feature)
            best_acc_bidir = best_candidate_acc
            changed = True
            print(f"[BIDIR REMOVE] {remove_feature:2d} -> {best_acc_bidir*100:.4f}%")

        if not changed:
            break

    # ========================= BEST POLICY =========================
    results = {
        "forward": (best_acc_forward, selected_forward),
        "backward": (best_acc_backward, selected_backward),
        "bidirectional": (best_acc_bidir, selected_bidir)
    }

    best_method = max(results.items(), key=lambda x: x[1][0])

    best_search = best_method[0]
    best_accuracy = best_method[1][0]
    best_features = sorted([int(i) for i in best_method[1][1]])

    print(f"\nBEST SEARCH FOR {clf_name}: {best_search.upper()}")
    print(f"Accuracy: {best_accuracy*100:.4f}%")
    print(f"Selected Features ({len(best_features)}): {best_features}")

    # ========================= TRAIN FINAL FULL MODEL =========================
    final_scaler = StandardScaler()
    X_best = final_scaler.fit_transform(X_raw[:, best_features])

    classifier.fit(X_best, y)

    save_object = {
        "classifier_name": clf_name,
        "model": classifier,
        "scaler": final_scaler,
        "selected_features": best_features,
        "search_policy": best_search,
        "cv_accuracy": best_accuracy,
        "label_classes": class_names
    }

    with open(output_dir / f"{clf_name}_model.pkl", "wb") as f:
        pickle.dump(save_object, f)

    all_results[clf_name] = {
        "accuracy": best_accuracy,
        "features": best_features,
        "search_policy": best_search
    }

# =========================================================
# SAVE MASTER RESULTS
# =========================================================
np.save(output_dir / "all_classifier_results.npy", all_results)

print("\n" + "="*80)
print("ALL CLASSIFIER MODELS SAVED SUCCESSFULLY")
print("="*80)