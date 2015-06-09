#!/usr/bin/env ruby

PROFILE_DIR="~/Library/MobileDevice/Provisioning Profiles"

require 'fileutils'
require 'io/console'
require 'optparse'

def update_developer_certificates(cert_name, cert_path, password)
  $stdout.puts "Removing all certs with name: '#{cert_name}'"
  cert_ids=`security find-certificate -a -Z -c "#{cert_name}" | grep SHA-1 | awk '{print $3}'`
  cert_ids.split(/\n/).each do |cert_id|
    $stdout.puts "Removing cert: '#{cert_id}'"
    `security delete-certificate -Z #{cert_id}`
  end

  $stdout.puts "Installing cert: '#{cert_path}'"
  `security import #{cert_path} -k ~/Library/Keychains/login.keychain -P #{password} -T /usr/bin/codesign`
end

def update_provisioning_profile(profile_path, profile_uuid)
  profile_dir = File.expand_path(PROFILE_DIR)
  FileUtils.mkdir_p profile_dir
  profile_path = File.expand_path(profile_path)
  install_path = "#{profile_dir}/#{profile_uuid}.mobileprovision"
  $stdout.puts "Installing #{profile_path} to #{install_path}"
  FileUtils.cp profile_path, install_path
end

options = {}
OptionParser.new do |opts|
  opts.banner = "Usage: install.rb [options]"

  opts.on("-c", "--clean", "Delete any existing provisioning profiles") do |c|
    options[:clean] = c
  end

  opts.on("-p", "--password PASSWORD", "Certificate password") do |password|
    options[:password] = password
  end
end.parse!

if !options[:password]
  puts "Enter Certificate Password:"
  options[:password] =  STDIN.noecho(&:gets).chomp || ""
  if options[:password].empty?
    fail "Certificate password is required."
  end
end

if options[:clean]
  puts "Cleaning all Provisioning Profiles."
  profile_dir = File.expand_path(PROFILE_DIR)
  Dir.glob("#{profile_dir}/**/*").each do |file|
    puts "Deleting #{file}"
    FileUtils.rm file
  end
end

puts "Installing standard certificates and profiles."
self_dir = File.expand_path(File.dirname(__FILE__))

# Installing Development Certificates
update_developer_certificates('iPhone Developer: wme-jenkins gen (26CW9V38S8)', "#{self_dir}/certs/wme-jenkins.gen-Certificates.p12", options[:password])

# Installing Development Profiles
update_provisioning_profile("#{self_dir}/profiles/WMEJenkinsgen_spark_profile.mobileprovision", "56d578a0-aad6-49b5-831d-281881fe0b51")
update_provisioning_profile("#{self_dir}/profiles/WMEJenkinsgen_profile.mobileprovision", "bc1fd10a-0282-472e-aebe-cb364d2ac5b1")

# Installing Distribution Profiles, certificates are also required.
update_provisioning_profile("#{self_dir}/profiles/SquaredAppStore.mobileprovision", "a58982b8-0569-4bec-8db2-25188ff71714")
update_provisioning_profile("#{self_dir}/profiles/WBXSQ.mobileprovision", "eb04ca36-25ef-4e70-bf09-fc11ad41318e")
