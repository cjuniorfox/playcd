{
  description = "PlayCD - Audio CD player for Linux";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        python = pkgs.python312;
        pythonPackages = python.pkgs;
      in
      {
        packages.default = pythonPackages.buildPythonApplication {
          pname = "playcd";
          version = "0.1.0";
          src = ./.;

          propagatedBuildInputs = with pythonPackages; [
            sounddevice
            pycdio
          ];

          nativeBuildInputs = with pkgs; [ pkg-config ];
          buildInputs = with pkgs; [ portaudio libcdio ];

          # Make playcd executable available
          entryPoints = {
            playcd = "playcd.playcd:main";
          };

          meta = with pkgs.lib; {
            description = "Audio CD player with pipe and keyboard control";
            homepage = "https://github.com/cjuniorfox/playcd";
            license = licenses.mit;
            maintainers = with maintainers; [ ];
          };
        };

        # Provide a NixOS module
        nixosModules.playcd = {
          options.services.playcd = {
            enable = pkgs.lib.mkEnableOption "PlayCD audio CD player";
            user = pkgs.lib.mkOption {
              type = pkgs.lib.types.str;
              default = "playcd";
              description = "User to run playcd as.";
            };
            device = pkgs.lib.mkOption {
              type = pkgs.lib.types.str;
              default = "/dev/sr0";
              description = "CD-ROM device to bind playcd to.";
            };
            
          };

          config = pkgs.lib.mkIf config.services.playcd.enable {
            users.users.${config.services.playcd.user} = {
              isSystemUser = true;
              home = "/var/lib/playcd";
            };

            systemd.services.playcd = {
              description = "Auto play CDs when inserted";
              bindsTo = [ "dev-sr0.device" ];
              after = [ "dev-sr0.device" "sound.target" ];
              wantedBy = [ "dev-sr0.device" ];

              serviceConfig = {
                ExecStart = "${self.packages.${system}.default}/bin/playcd";
                ExecStopPost = "${pkgs.util-linux}/bin/eject ${config.services.playcd.device}";
                Restart = "on-failure";
                User = config.services.playcd.user;
              };
            };
          };
        };
      });
}
