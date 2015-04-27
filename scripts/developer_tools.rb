#!/usr/bin/env ruby

require 'fileutils'

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

  profile_dir = File.expand_path("~/Library/MobileDevice/Provisioning Profiles")
  #remove the old provision
  #FileUtils.rm_rf profile_dir
  FileUtils.mkdir_p profile_dir
  profile_path = File.expand_path(profile_path)

  install_path = "#{profile_dir}/#{profile_uuid}.mobileprovision"
  $stdout.puts "Installing #{profile_path} to #{install_path}"
  FileUtils.cp profile_path, install_path
end

password = ARGV[0]
if password.nil?
  puts "Invalid Parameters: developer_tools.rb certificate_password [certificate_name] [certificate_path] [provisioning_profile_path] [provisioning_profile_uuid]"
  exit -1
end

cert_name = ARGV[1]
cert_path = ARGV[2]
profile_path = ARGV[3]
profile_uuid = ARGV[4]

if cert_name.nil? || cert_path.nil? || profile_path.nil? || profile_uuid.nil?
  puts "Installing standard certificates and profiles."
  current_dir = File.expand_path(File.join(File.dirname(__FILE__), '..'))

  # Installing Development Certificates
  update_developer_certificates('iPhone Developer: wme-jenkins gen (26CW9V38S8)', "#{current_dir}/wme-jenkins.gen-Certificates.p12", password)

  # Installing Development Profiles
  update_provisioning_profile("#{current_dir}/WMEJenkinsgen_profile.mobileprovision", "3905ba37-d231-4e39-8fd8-f410d79346df")

else
  puts "Installing specified certificate and profile"
  update_developer_certificates(cert_name, cert_path, password)
  update_provisioning_profile(profile_path, profile_uuid)
end

exit 0
