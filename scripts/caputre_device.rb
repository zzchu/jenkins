#!/usr/bin/env ruby


require_relative './idevicehelpers.rb'

device_udids = Idevice.device_list

id_str=""
device_udids.each do |device_udid|
	$stdout.puts "Found ios device: #{device_udid}"
	id_str+=device_udid+","
end
id_str=id_str[0..-2]
File.open("ios_id", 'w') { |file| file.write(id_str) }