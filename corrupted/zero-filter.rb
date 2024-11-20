require "pnglitch"

PNGlitch.open("challenge.png") do |png|
  png.each_scanline do |line|
    line.graft 0
  end
  png.save "challenge-zero-filter.png"
end
