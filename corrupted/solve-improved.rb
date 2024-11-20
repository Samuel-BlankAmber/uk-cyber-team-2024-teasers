require "pnglitch"

PNGlitch.open("challenge.png") do |png|
  png.each_scanline do |line|
    if line.filter_type == 2
      line.graft 1
    end
  end
  png.save "challenge-restored-improved.png"
end
