--  This script does 2 things in an attemtp to repari the Instruemtns and related
-- daemons on macos.  1) It laucnhes xcode and opens the devices window which connect
-- to the iphone to show the device log
-- 2) It laucnhes Instruments which will be set to instrumenting the iphone 
-- FYI - Both the devices widnows and instruments remember which device you want to
-- view, so please make sure you manually set both to look at the iphone, at least once

tell application "Xcode" to activate

tell application "System Events"
	tell process "Xcode"
		set frontmost to true
		
		keystroke "2" using {shift down, command down}
		delay 4.0
		set organizer to window 1
	end tell
end tell


tell application "System Events"
	tell process "Xcode"
		tell menu bar 1
			tell menu bar item "Xcode"
				tell menu 1
					tell menu item "Open Developer Tool"
						tell menu 1
							click menu item "Instruments"
						end tell
					end tell
				end tell
			end tell
		end tell
	end tell
end tell


-- Give time for Instruments to launch and run and hopefully communicate with the iphone
delay 10

tell application "Instruments" to quit
tell application "Xcode" to quit
