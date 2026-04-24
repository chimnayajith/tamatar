{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    nodejs_20
    nodePackages.npm
    python311
    python311Packages.pip
    cudaPackages.cudatoolkit
    cudaPackages.cudnn
    stdenv.cc.cc
  ];

  shellHook = ''
    export LD_LIBRARY_PATH=/run/opengl-driver/lib:${pkgs.stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH

    echo "Node.js development environment loaded"
    echo "Node version: $(node --version)"
    echo "NPM version: $(npm --version)"
    echo ""
    echo "Project: Tamatar - Tomato Leaf Disease Detection PWA"
    echo ""
  '';
}
