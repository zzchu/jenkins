#!/usr/bin/env ruby


require_relative './idevicehelpers.rb'

device_udids = Idevice.device_list

device_udids.each do |device_udid|
	$stdout.puts "Found ios device: #{device_udid}"
end