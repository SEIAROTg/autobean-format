{
  description = "Packaging for autobean-format";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = inputs:
    inputs.flake-utils.lib.eachDefaultSystem
      (system:
        let
          pkgs = import inputs.nixpkgs {
            inherit system;
          };

          autobean-refactor =
            let
              version = "0.2.6";
              # The hash will need to be updated when the version is bumped.
              # The easiest way is to set it to the empty string and observe the output of nix build.
              hash = "sha256-F5mIsMLU5o7+sKmu+r4CmHrImGnfPkaPOv/WJNtSErM=";
            in
            pkgs.python3Packages.buildPythonPackage {
              pname = "autobean-refactor";
              inherit version;
              pyproject = true;
              src = pkgs.fetchFromGitHub {
                owner = "SEIAROTg";
                repo = "autobean-refactor";
                rev = "v${version}";
                inherit hash;
              };

              nativeBuildInputs = with pkgs.python3Packages; [
                pdm-pep517
              ];

              propagatedBuildInputs = with pkgs.python3Packages; [
                lark
                typing-extensions
              ];
            };

          autobean-format =
            let
              pyproject = (builtins.fromTOML (builtins.readFile ./pyproject.toml));
              version = pyproject.project.version;
            in
            pkgs.python3Packages.buildPythonApplication {
              pname = "autobean-format";
              inherit version;
              pyproject = true;
              src = ./.;

              nativeBuildInputs = with pkgs.python3Packages; [
                pdm-pep517
              ];

              propagatedBuildInputs = with pkgs.python3Packages;[
                autobean-refactor
                typing-extensions
              ];
            };
        in
        {
          packages.default = autobean-format;
        }
      );
}
