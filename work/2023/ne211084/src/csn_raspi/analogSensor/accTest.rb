require 'pi_piper'
loop do
  value = 0
  PiPiper::Spi.begin do |spi|
    #raw = spi.write [0b01101000,0]
    raw = spi.write [0b01111000,0]
    value = ((raw[0]<<8) + raw[1]) & 0x03FF
  end
  volt = (value * 3300)/1024
  gal = volt - 1650
  acc = gal / 660
  degree = (volt - 500)/10
  #puts degree
  puts acc
  sleep(1)
end
