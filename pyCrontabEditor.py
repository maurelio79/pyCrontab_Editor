#!/usr/bin/env python
   
import pygtk
pygtk.require('2.0')
import gtk, gobject
import os

uid = os.getuid()
if (uid > 0):
	dialogError = gtk.MessageDialog(None, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
	dialogError.set_markup("You are not root! Run this script with root account.\nBye!")
	dialogError.run()
	dialogError.destroy()
	quit()
			
def display_error(data):
	dialogError = gtk.MessageDialog(None, type=gtk.MESSAGE_ERROR, buttons=gtk.BUTTONS_OK)
	dialogError.set_markup(data)
	dialogError.run()
	dialogError.destroy()

class CrontabEditor:
	def delete_event(self, widget, data):
		print "Exiting..."
		gtk.main_quit()
		return False
		
	def see_crontab(self, widget):
		os.system("cat /etc/crontab | zenity --text-info --title='/etc/crontab' --width='640' --height='480'")
		
	def choose_user(obj, widget):
		user = obj.comboUser.get_active()
		if (user == 1):
			obj.inputUser.show()
		else:
			obj.inputUser.hide()
			
	def choose_time(obj, widget):
		time = obj.comboTime.get_active()
		if (time == 0):
			obj.spinHour.hide()
			obj.boxWeekly.hide()
			obj.boxMonthly.hide()
			obj.timeLabel.set_text("Which Minute of every hour?")
			obj.radioHourly.set_active(True)
		elif (time == 1):
			obj.boxMonthly.hide()
			obj.boxWeekly.hide()
			obj.timeLabel.set_text("What time?")
			obj.spinHour.show()
			obj.radioDayly.set_active(True)
		elif (time == 2):
			obj.boxMonthly.hide()
			obj.timeLabel.set_text("What time?")
			obj.spinHour.show()
			obj.boxWeekly.show()
			obj.radioWeekly.set_active(True)
		elif (time == 3):
			obj.timeLabel.set_text("What time?")
			obj.boxWeekly.hide()
			obj.spinHour.show()
			obj.boxMonthly.show()
			obj.radioMonthly.set_active(True)
			
	def start_event(obj, widget):
		os.system("cp -a /etc/crontab /etc/crontab.bak")
		script = obj.buttonFile.get_filename()
		if not script:
			display_error("Script File not defined")
			return 1
		
		if (obj.checkButton.get_active() == True):
			os.system("cp -a " + script + " /usr/local/bin/" )
			script = os.path.basename(script)
			script = "/usr/local/bin/" + script
			
		if (obj.comboUser.get_active() == 0):
			user = "root"
		else:
			user = obj.inputUser.get_text()
			if (user == "Insert here other user"):
				display_error("Choose a valid user")
				return 1
			elif (user == ""):
				display_error("Choose a valid user")
				return 1
				
		mon = "*"
		if (obj.radioHourly.get_active() == True):
			m = str(obj.spinMinute.get_value_as_int())
			h = "*"
			dom = "*"
			dow = "*"
		elif (obj.radioDayly.get_active() == True):
			m = str(obj.spinMinute.get_value_as_int())
			h = str(obj.spinHour.get_value_as_int())
			dom = "*"
			dow = "*"
		elif (obj.radioWeekly.get_active() == True):
			m = str(obj.spinMinute.get_value_as_int())
			h = str(obj.spinHour.get_value_as_int())
			dom = "*"
			dow = str(obj.comboWeekly.get_active())
		elif 	(obj.radioMonthly.get_active() == True):
			m = str(obj.spinMinute.get_value_as_int())
			h = str(obj.spinHour.get_value_as_int())
			dom = str(obj.spinMonthly.get_value_as_int())
			dow = "*"
			
		#print m
		#print h
		#print dom
		#print mon
		#print dow
		
		crontab = open("/etc/crontab", "a")
		crontab.write("\n# Inserted with Crontab Editor\n")
		crontab.write(m + "  " + h + "  " + dom + "  " + mon + "  " + dow + "    " + user + "    " + script + "\n")
		crontab.close()
		
			
	def __init__(self):

		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_title("Crontab Editor")
		self.window.set_border_width(25)
		#self.window.set_resizable(False)
		self.window.set_default_size(440, -1)

		self.window.connect("delete_event", self.delete_event)
		
		self.adj1 = gtk.Adjustment(0, 0, 23, 1, 10, 0)
		self.adj2 = gtk.Adjustment(0, 0, 59, 1, 10, 0)
		self.adj3 = gtk.Adjustment(1, 1, 31, 1, 10, 0)

		self.boxContainer = gtk.VBox(False, 15)
		self.window.add(self.boxContainer)
		self.boxContainer.show()
		
		self.descriptionLabel = gtk.Label("Select script to add in crontab, set data as you need then click Apply.\nFor your security i will copy the original file to /etc/crontab.bak\n")
		self.boxContainer.pack_start(self.descriptionLabel)
		self.descriptionLabel.show()
		
		self.fileLabel = gtk.Label("Select script to add in crontab\t\t\t\t\t\t\t\t")
		self.boxContainer.pack_start(self.fileLabel)
		self.fileLabel.show()
		
		# Box with button file and checkbutton
		self.box1 = gtk.HBox(False, 5)
		self.boxContainer.pack_start(self.box1)
		self.box1.show()
		
		self.buttonFile = gtk.FileChooserButton("Choose script file to add in crontab")
		self.box1.pack_start(self.buttonFile, True)
		self.buttonFile.show()
		
		self.checkButton = gtk.CheckButton()
		self.checkButton.set_label("I want copy the script in /usr/local/bin")
		self.box1.pack_start(self.checkButton, False)
		self.checkButton.show()
		
		# Widget for user choosing
		self.userLabel = gtk.Label("Script will run under user...")
		self.boxContainer.pack_start(self.userLabel, True)
		self.userLabel.show()
				
		self.comboUser = gtk.combo_box_new_text()
		self.comboUser.append_text("root")
		self.comboUser.append_text("other")
		self.comboUser.set_active(0)
		self.boxContainer.pack_start(self.comboUser, True)
		self.comboUser.show()
		
		self.inputUser = gtk.Entry()
		self.inputUser.set_text("Insert here other user")
		self.boxContainer.pack_start(self.inputUser, True)
		
		# Here start crontab variables
		self.whenLabel = gtk.Label("Run this script every...")
		self.boxContainer.pack_start(self.whenLabel, True)
		self.whenLabel.show()
		
		self.comboTime = gtk.combo_box_new_text()
		self.comboTime.append_text("Every Hour")
		self.comboTime.append_text("Every Day")
		self.comboTime.append_text("Every Week")
		self.comboTime.append_text("Every Month")
		self.comboTime.set_active(0)
		self.boxContainer.pack_start(self.comboTime, True)
		self.comboTime.show()
		
		# Box will show if selected weekly in comboTime
		self.boxWeekly = gtk.VBox(False, 5)
		self.boxContainer.pack_start(self.boxWeekly)

		self.weeklyLabel = gtk.Label("Wich day of week?")
		self.boxWeekly.pack_start(self.weeklyLabel, True)
		self.weeklyLabel.show()
		
		self.comboWeekly = gtk.combo_box_new_text()
		self.comboWeekly.append_text("Sunday")
		self.comboWeekly.append_text("Monday")
		self.comboWeekly.append_text("Tuesday")
		self.comboWeekly.append_text("Wendsday")
		self.comboWeekly.append_text("Thursday")
		self.comboWeekly.append_text("Friday")
		self.comboWeekly.append_text("Saturday")
		self.comboWeekly.set_active(0)
		self.boxWeekly.pack_start(self.comboWeekly, True)
		self.comboWeekly.show()
		
		# Box will show if selected monthly in comboTime
		self.boxMonthly = gtk.VBox(False, 5)
		self.boxContainer.pack_start(self.boxMonthly)

		self.monthlyLabel = gtk.Label("Wich day of month?")
		self.boxMonthly.pack_start(self.monthlyLabel, True)
		self.monthlyLabel.show()
		
		self.spinMonthly = gtk.SpinButton(self.adj3)
		self.boxMonthly.pack_start(self.spinMonthly, True)
		self.spinMonthly.show()
		
		# This label change dinamically
		self.timeLabel = gtk.Label("Which minute of every hour?")
		self.boxContainer.pack_start(self.timeLabel, True)
		self.timeLabel.show()
		
		self.boxHM = gtk.HBox(False, 5)
		self.boxContainer.pack_start(self.boxHM)
		self.boxHM.show()
		
		#spinHour will hide only if in comboTime user choose hourly
		self.spinHour = gtk.SpinButton(self.adj1)
		self.boxHM.pack_start(self.spinHour, True)
		
		self.spinMinute = gtk.SpinButton(self.adj2)
		self.boxHM.pack_start(self.spinMinute, True)
		self.spinMinute.show()
		
		self.bottomBox = gtk.HBox(False, 5)
		self.boxContainer.pack_start(self.bottomBox)
		self.bottomBox.show()
		
		self.quitButton = gtk.Button("Quit")
		self.bottomBox.pack_start(self.quitButton)
		self.quitButton.show()
		
		self.crontabButton = gtk.Button("See Crontab File")
		self.bottomBox.pack_start(self.crontabButton)
		self.crontabButton.show()
		
		self.submitButton = gtk.Button("Apply")
		self.bottomBox.pack_start(self.submitButton)
		self.submitButton.show()
		
		# This will never show, just usefull for me!
		self.radioHourly = gtk.RadioButton(None, "")
		self.bottomBox.pack_start(self.radioHourly, True)
		self.radioHourly.set_active(True)
		#self.radioHourly.show()
		self.radioDayly = gtk.RadioButton(self.radioHourly, "")
		self.bottomBox.pack_start(self.radioDayly, True)
		#self.radioDayly.show()
		self.radioWeekly = gtk.RadioButton(self.radioHourly, "")
		self.bottomBox.pack_start(self.radioWeekly, True)
		#self.radioWeekly.show()
		self.radioMonthly = gtk.RadioButton(self.radioHourly, "")
		self.bottomBox.pack_start(self.radioMonthly, True)
		#self.radioMonthly.show()

		
		# Here every handler
		self.comboUser.connect("changed", self.choose_user)
		self.comboTime.connect("changed", self.choose_time)
		self.submitButton.connect("clicked", self.start_event)
		self.crontabButton.connect("clicked", self.see_crontab)
		self.quitButton.connect("clicked", self.delete_event, None)
		
		self.window.show()
		
	def main(self):
		gtk.main()
		
if __name__ == "__main__":
	crontabeditor = CrontabEditor()
	crontabeditor.main()
		
