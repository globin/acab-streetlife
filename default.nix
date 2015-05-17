with import <nixpkgs> {};
with pkgs.python27Packages;

stdenv.mkDerivation {
  name = "acab";
  buildInputs = [
    python
    pygame
    wxPython
    procps
    pyaudio
    numpy
    pil
  ];
}
