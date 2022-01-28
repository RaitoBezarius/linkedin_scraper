{ pkgs ? import <nixpkgs> {} }:
rec {
  package = pkgs.python3.pkgs.buildPythonPackage {
    pname = "linkedin_scraper";
    version = "2.4.0";
    src = ./.;
    doCheck = false;
    propagatedBuildInputs = with pkgs.python3.pkgs; [
      selenium
      lxml
      requests
    ];
  };

  shell = pkgs.mkShell {
    buildInputs = [
      (pkgs.python3.withPackages (ps: [ package ps.ipython ]))
      pkgs.chromedriver
    ];
  };
}
