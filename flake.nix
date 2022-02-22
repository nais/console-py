{
  description = "Application packaged using poetry2nix";

  inputs = {
    utils.url = "flake:flake-utils";
    nixpkgs.url = "flake:nixpkgs";
    poetry2nix.url = "flake:poetry2nix";
  };

  outputs = {
    self
    , nixpkgs
    , utils
    , poetry2nix
  }: let
    defaultPythonSetup = {
      projectDir = ./.;
      python = nixpkgs.legacyPackages.x86_64-linux.python39;
    };
  in {
    # Nixpkgs overlay providing the application
    overlay = nixpkgs.lib.composeManyExtensions [
      poetry2nix.overlay (
        final: prev: {
          # The application
          app = prev.poetry2nix.mkPoetryApplication (
            {
              overrides = prev.poetry2nix.defaultPoetryOverrides.extend (
                self: super: {
                  prospector = super.prospector.overridePythonAttrs (
                    old: {
                      buildInputs = (old.buildInputs or [ ]) ++ [self.poetry];
                    }
                  );
                }
              );
            } // defaultPythonSetup
          );
        }
      )
    ];
  } // (utils.lib.eachDefaultSystem (
    system: let
      pkgs = import nixpkgs {
        inherit system;
        overlays = [self.overlay];
      };
    in {
      defaultApp = pkgs.app;
      defaultPackage = self.defaultApp."${system}";
      devShell = with pkgs; mkShell {
        buildInputs = [
          defaultPythonSetup.python
          postgresql
        ];
      };
    }
  ));
}
