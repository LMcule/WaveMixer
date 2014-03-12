#!/usr/bin/env python
import pyaudio
import wave
import sys
import time, wave
from Tkinter import *
import tkFileDialog
from tkFileDialog import askopenfilename
import struct

SHRT_MIN=-32767 - 1
SHRT_MAX=32767
finWidth=None
wf=None
outFile="output.wav"
fout=None
fmts=(None, "=B", "=h", None, "=l")
dcs=(None, 128, 0, None, 0)

def callback(in_data, frame_count, time_info, flags):
	
	global pause
	data = wf.readframes(frame_count)
	if(pause==0):
		return (data, pyaudio.paContinue)
	if(pause==1):
		return (data, pyaudio.paAbort)

fileNames = {}
fileNames['wave1']="No File Selected"
root=Tk()
var1 = StringVar()
var2 = StringVar()
var3 = StringVar()
var1.set('No File Selected')
var2.set('No File Selected')
var3.set('No File Selected')
var_reversal1 = IntVar()
var_modulation1 = IntVar()
var_mix1 = IntVar()
var_reversal2 = IntVar()
var_modulation2 = IntVar()
var_mix2 = IntVar()
var_reversal3 = IntVar()
var_modulation3 = IntVar()
var_mix3 = IntVar()
time_record=None
stream=None
pause=0
p=None
w=None
amp_bar1=None	
shift_bar1=None	
scale_bar1=None	
amp_bar2=None	
shift_bar2=None	
scale_bar2=None	
amp_bar3=None	
shift_bar3=None	
scale_bar3=None	
scaleFactor=1	
def pause_func():
	global pause
	pause=1
 	# song_func()
def play_func(playType):
	global pause
	global isReversal
	pause=0
	#if var_modulation1.get()==1 or var_modulation2.get()==1 or var_modulation3.get()==1:
	#	modulateWaves()
		
	if playType!=5:	
		readFile(playType)
		ampScaling(ampFactor)
		timeShifting(shiftFactor)
		print "scaling"
		print scaleFactor
		timeScaling(scaleFactor)
		if(isReversal):
			timeReversal()
		pack_file()
	song_func(playType)
	
def modulateAndPlayFunc():
	global pause
	pause=0
	print "IN MIX"
	if var_modulation1.get()==1 or var_modulation2.get()==1 or var_modulation3.get()==1:
		modulateWaves()
		pack_file()
		#4 -> Mix and Play
		song_func(4)
	else:
		print "No Waves Selected"
def mixAndPlayFunc():
	global pause
	pause=0
	print "IN MIX"
	if var_mix1.get()==1 or var_mix2.get()==1 or var_mix3.get()==1:
		mixWaves()
		pack_file()
		#4 -> Mix and Play
		song_func(4)
	else:
		print "No Waves Selected"
max_wave=0
min_wave=0
def modulateWaves():
	global min_wave
	min_len=1000000000000000
	
	global data
	global fin
	wave1_data=None
	wave2_data=None
	wave3_data=None


	count=0
	data=[]
	if var_modulation1.get()==1 and not (fileNames['wave1'] == 'No File Selected'):
		print "Mixing 1"
		count+=1
		readFile(1)
		print data[0]
		ampScaling(ampFactor)
		timeShifting(shiftFactor)
		timeScaling(scaleFactor)
		if(isReversal):
			timeReversal()
		wave1_data=data
		print wave1_data[0]
		if(len(data)<min_len):
			min_len=len(data)
			min_wave=1
			fin.close()
		    	some=fileNames['wave1']
        		fin = wave.open(some, 'rb')
			
	data=[]
	if var_modulation2.get()==1 and not (fileNames['wave2'] == 'No File Selected'):
		count+=1
		readFile(2)
		ampScaling(ampFactor)
		timeShifting(shiftFactor)
		timeScaling(scaleFactor)
		if(isReversal):
			timeReversal()
		wave2_data=data
		if(len(data)<min_len):
			min_len=len(data)
			min_wave=2
		    	some=fileNames['wave2']
			fin.close()
        		fin = wave.open(some, 'rb')
	data=[]
	if var_modulation3.get()==1 and not (fileNames['wave3'] == 'No File Selected'):
		print 'hey'
		count+=1
		readFile(3)
		ampScaling(ampFactor)
		timeShifting(shiftFactor)
		timeScaling(scaleFactor)
		if(isReversal):
			timeReversal()
		wave3_data=data
		if(len(data)<min_len):
			min_len=len(data)
			min_wave=3
			fin.close()
		    	some=fileNames['wave3']
        		fin = wave.open(some, 'rb')
	val1=1
	val2=1
	val3=1
	data=[]
	for i in xrange(min_len):
			if wave1_data:
				val1=wave1_data[i]

			if wave2_data:
				val2=wave2_data[i]
			if wave3_data:
				val3=wave3_data[i]

			if val1*val2*val3>SHRT_MAX:
				data.append(SHRT_MAX)
			elif val1*val2*val3<SHRT_MIN:
				data.append(SHRT_MIN)
			else:
				data.append(val1*val2*val3/count)


def mixWaves():
	global max_wave
	max_len=-10000
	
	global data
	global fin
	wave1_data=None
	wave2_data=None
	wave3_data=None


	count=0
	data=[]
	if var_mix1.get()==1 and not (fileNames['wave1'] == 'No File Selected'):
		print "Mixing 1"
		count+=1
		readFile(1)
		print data[0]
		ampScaling(ampFactor)
		timeShifting(shiftFactor)
		timeScaling(scaleFactor)
		if(isReversal):
			timeReversal()
		wave1_data=data
		print wave1_data[0]
		if(len(data)>max_len):
			max_len=len(data)
			print "1 Length of array " +str(max_len)
			max_wave=1
			fin.close()
		    	some=fileNames['wave1']
        		fin = wave.open(some, 'rb')
			
	print wave1_data[0]

	print 'som up'
	print wave1_data[0]
	#del data[:]	
	data=[]
	if var_mix2.get()==1 and not (fileNames['wave2'] == 'No File Selected'):
		print 'why'
		count+=1
		readFile(2)
		ampScaling(ampFactor)
		timeShifting(shiftFactor)
		timeScaling(scaleFactor)
		if(isReversal):
			timeReversal()
		wave2_data=data
		if(len(data)>max_len):
			max_len=len(data)
			max_wave=2
		    	some=fileNames['wave2']
			fin.close()
        		fin = wave.open(some, 'rb')
	print 'up'
	print wave1_data[0]
	data=[]
	if var_mix3.get()==1 and not (fileNames['wave3'] == 'No File Selected'):
		print 'hey'
		count+=1
		readFile(3)
		ampScaling(ampFactor)
		timeShifting(shiftFactor)
		timeScaling(scaleFactor)
		if(isReversal):
			timeReversal()
		wave3_data=data
		if(len(data)>max_len):
			max_len=len(data)
			max_wave=3
			fin.close()
		    	some=fileNames['wave3']
        		fin = wave.open(some, 'rb')
	val1=0
	val2=0
	val3=0
	data=[]
	for i in xrange(max_len):
			if wave1_data:
				if i>=len(wave1_data):
					val1=0
				else:
					val1=wave1_data[i]

			if wave2_data:
				if i>=len(wave2_data):
					val2=0
				else:
					val2=wave2_data[i]
			if wave3_data:
				if i>=len(wave3_data):
					val3=0
				else:
					val3=wave3_data[i]

			if val1+val2+val3>SHRT_MAX:
				data.append(SHRT_MAX)
			elif val1+val2+val3<SHRT_MIN:
				data.append(SHRT_MIN)
			else:
				data.append(val1+val2+val3/count)
	print "finaldata"
	print data[0]
	print "End finaldata"

		
def song_func(playType):
		global stream
		global fileNames
		global wf
		global p
		global pause
		if (playType==1 and not (fileNames['wave1'] == 'No File Selected')) or (playType==2 and not (fileNames['wave2'] == 'No File Selected')) or (playType==3 and not (fileNames['wave3'] == 'No File Selected')) or playType==4 or playType==5:	
							
				# open the file for reading.
				# wf = wave.open(fileName, 'r')
				wf = wave.open(outFile, 'r')
				# create an audio object
				p = pyaudio.PyAudio()
				print wf.getsampwidth()
		
				# open stream based on the wave object which has been input.
				stream = p.open(format =
        			  	p.get_format_from_width(wf.getsampwidth()),
        			       	channels = wf.getnchannels(),
       			 	       	rate = wf.getframerate(),
					output = True,
					stream_callback=callback)
				stream.start_stream()
				root.mainloop()
				#createWidgets()

def createWidgets():
			global w
			global amp_bar1
			global shift_bar1
			global scale_bar1
			global var_reversal1
			global var_modulation1
			global var_mix1
			global amp_bar2
			global shift_bar2
			global scale_bar2
			global var_reversal2
			global var_modulation2
			global var_mix2
			global amp_bar3
			global shift_bar3
			global scale_bar3
			global var_reversal3
			global var_modulation3
			global var_mix3
			global time_record
			menubar = Menu(root)
			root.config(menu=menubar)
			root.minsize(300,300)
			w = 1000
			h = 600
			x = 150
			y = 100
			# use width x height + x_offset + y_offset (no spaces!)
			root.geometry("%dx%d+%d+%d" % (w, h, x, y))
			#		root.geometry("500x500")
			root.wm_title("Wave Mixer")
			filemenu = Menu(menubar, tearoff=0)
			filemenu.add_command(label="Exit", command=root.quit)
			menubar.add_cascade(label="File", menu=filemenu)
			w = Label(root, text="Wave Mixer", font=("Helvetica", 16))
			w.pack()
			w1 = Canvas(root, width=30000, height=15)
			w1.pack()
			# update is needed
			root.update()
			geo = root.geometry()
			print(geo) # 460x320+150+100
			Width = root.winfo_width() # 460
			print(Width)
			Height = root.winfo_height() # 320
			print(Height)
			w1.create_line(0,10,root.winfo_width()+1000, 10)
			

		
			#Frame 1
			
			labelframe1 = LabelFrame(root, text="Wave 1")
			labelframe1.pack(fill='both',expand='yes')
			labelframe1.place( x=100, y=55,width=Width/4-Width/80,height=Height-Height/3) 
			
			some=Button(labelframe1, text='Choose File', command= lambda: askopenfile(1))
			some.pack()
			
			left1 = Label(labelframe1, textvariable=var1)
			left1.pack()
						
			amp1 = Label(labelframe1, text="Amplitude")
			amp1.pack()
			amp1.place( x=5, y=55) 
			amp_bar1 = Scale(labelframe1, from_=0, to=5,sliderlength=15, orient=HORIZONTAL)
			amp_bar1.pack()
			amp_bar1.place( x=50, y=70) 
			
			time_shift1 = Label(labelframe1, text="Time Shift")
			time_shift1.pack()
			time_shift1.place( x=5, y=115) 
			shift_bar1 = Scale(labelframe1, from_=-1, to=1,resolution=0.1,sliderlength=15, orient=HORIZONTAL)
			shift_bar1.pack()
			shift_bar1.place( x=50, y=130) 
			
			
			time_scale1 = Label(labelframe1, text="Time Scaling")
			time_scale1.pack()
			time_scale1 .place( x=5, y=175) 
			scale_bar1 = Scale(labelframe1, from_=0, to=10,sliderlength=15,resolution=0.05, orient=HORIZONTAL)
			scale_bar1.pack()
			scale_bar1.place( x=50, y=190)


			reversal1 = Checkbutton(labelframe1, text="Time Reversal", variable=var_reversal1)
			reversal1.pack()
			reversal1.place( x=5, y=250)

			modulation1 = Checkbutton( labelframe1, text="Select for Modulation", variable=var_modulation1)
			modulation1.pack()
			modulation1.place( x=5, y=275)
			
			mix1 = Checkbutton(labelframe1, text="Select for Mixing", variable=var_mix1)
			mix1.pack()
			mix1.place( x=5, y=300)

			
			play1=Button(labelframe1, text='Play',command= lambda: play_func(1))
			play1.pack()
			play1.place( x=5, y=350) 
			
			pause=Button(labelframe1, text='Stop',command=pause_func)
			pause.pack()
			pause.place( x=55, y=350) 

			#Frame 2
			labelframe2 = LabelFrame(root, text="Wave 2",width=Width)
			labelframe2.pack(fill='both',expand='yes')
			labelframe2.place( x=100+Width/4+Width/80, y=55, width=Width/4-Width/80, height=Height-Height/3) 
		
			some2=Button(labelframe2, text='Choose File', command= lambda: askopenfile(2))
			some2.pack()
			
			left2 = Label(labelframe2, textvariable=var2)
			left2.pack()
						
			amp2 = Label(labelframe2, text="Amplitude")
			amp2.pack()
			amp2.place( x=5, y=55) 
			amp_bar2 = Scale(labelframe2, from_=0, to=5,sliderlength=15, orient=HORIZONTAL)
			amp_bar2.pack()
			amp_bar2.place( x=50, y=70) 
			
			time_shift2 = Label(labelframe2, text="Time Shift")
			time_shift2.pack()
			time_shift2.place( x=5, y=115) 
			shift_bar2 = Scale(labelframe2, from_=-1, to=1,resolution=0.1,sliderlength=15, orient=HORIZONTAL)
			shift_bar2.pack()
			shift_bar2.place( x=50, y=130) 
			
			
			time_scale2 = Label(labelframe2, text="Time Scaling")
			time_scale2.pack()
			time_scale2 .place( x=5, y=175) 
			scale_bar2 = Scale(labelframe2, from_=0, to=10,sliderlength=15,resolution=0.05, orient=HORIZONTAL)
			scale_bar2.pack()
			scale_bar2.place( x=50, y=190)


			reversal2 = Checkbutton(labelframe2, text="Time Reversal", variable=var_reversal2)
			reversal2.pack()
			reversal2.place( x=5, y=250)

			modulation2 = Checkbutton( labelframe2, text="Select for Modulation", variable=var_modulation2)
			modulation2.pack()
			modulation2.place( x=5, y=275)
			
			mix2 = Checkbutton(labelframe2, text="Select for Mixing", variable=var_mix2)
			mix2.pack()
			mix2.place( x=5, y=300)

			
			play2=Button(labelframe2, text='Play',command= lambda: play_func(2))
			play2.pack()
			play2.place( x=5, y=350) 
			
			pause2=Button(labelframe2, text='Stop',command=pause_func)
			pause2.pack()
			pause2.place( x=55, y=350) 


			#Frame 3
			labelframe3 = LabelFrame(root, text="Wave 3",width=Width)
			labelframe3.pack(fill='both',expand='yes')
			labelframe3.place( x=100+2*Width/4+2*Width/80, y=55, width=Width/4-Width/80, height=Height-Height/3) 
			

			some2=Button(labelframe3, text='Choose File', command= lambda: askopenfile(3))
			some2.pack()
			
			left3 = Label(labelframe3, textvariable=var3)
			left3.pack()
						
			amp3 = Label(labelframe2, text="Amplitude")
			amp3.pack()
			amp3.place( x=5, y=55) 
			amp_bar3 = Scale(labelframe3, from_=0, to=5,sliderlength=15, orient=HORIZONTAL)
			amp_bar3.pack()
			amp_bar3.place( x=50, y=70) 
			
			time_shift3 = Label(labelframe3, text="Time Shift")
			time_shift3.pack()
			time_shift3.place( x=5, y=115) 
			shift_bar3 = Scale(labelframe3, from_=-1, to=1,resolution=0.1,sliderlength=15, orient=HORIZONTAL)
			shift_bar3.pack()
			shift_bar3.place( x=50, y=130) 
			
			
			time_scale3 = Label(labelframe3, text="Time Scaling")
			time_scale3.pack()
			time_scale3 .place( x=5, y=175) 
			scale_bar3 = Scale(labelframe3, from_=0, to=10,sliderlength=15,resolution=0.05, orient=HORIZONTAL)
			scale_bar3.pack()
			scale_bar3.place( x=50, y=190)


			reversal3 = Checkbutton(labelframe3, text="Time Reversal", variable=var_reversal3)
			reversal3.pack()
			reversal3.place( x=5, y=250)

			modulation3 = Checkbutton( labelframe3, text="Select for Modulation", variable=var_modulation3)
			modulation3.pack()
			modulation3.place( x=5, y=275)
			
			mix3 = Checkbutton(labelframe3, text="Select for Mixing", variable=var_mix3)
			mix3.pack()
			mix3.place( x=5, y=300)

			
			play3=Button(labelframe3, text='Play',command= lambda: play_func(3))
			play3.pack()
			play3.place( x=5, y=350) 
			
			pause3=Button(labelframe3, text='Stop',command=pause_func)
			pause3.pack()
			pause3.place( x=55, y=350) 
			
			
			mixnplay = Label(root, text="MIX 'n' PLAY", font=("Helvetica", 12))
			mixnplay.pack()
			mixnplay.place( x=150, y=470) 
			
			play4=Button(root, text='Play',command= mixAndPlayFunc)
			play4.pack()
			play4.place( x=140, y=510) 
			
			pause4=Button(root, text='Stop',command=pause_func)
			pause4.pack()
			pause4.place( x=210, y=510) 

			mixnplay = Label(root, text="MODULATE 'n' PLAY", font=("Helvetica", 12))
			mixnplay.pack()
			mixnplay.place( x=100+2*Width/4+2*Width/80+40, y=470) 
			
			play4=Button(root, text='Play',command= modulateAndPlayFunc)
			play4.pack()
			play4.place( x=100+2*Width/4+2*Width/80 +80, y=510) 
			
			pause4=Button(root, text='Stop',command=pause_func)
			pause4.pack()
			pause4.place( x=100+2*Width/4+2*Width/80+140, y=510) 
			
			
			record_label = Label(root, text="RECORD 'n' PLAY", font=("Helvetica", 12))
			record_label.pack()
			record_label.place( x=400, y=470) 

			start_record=Button(root, text='Start',command= record)
			start_record.pack()
			start_record.place( x=400, y=530) 
			
			play_record=Button(root, text='Play',command= lambda: play_func(5))
			play_record.pack()
			play_record.place( x=500, y=530) 

			time_label = Label(root, text="Set Recording Time", font=("Helvetica", 8))
			time_label.pack()
			time_label.place( x=400, y=500) 			

			time_record = Spinbox(root, from_=1, to=30,width=3)
			time_record.pack()	
			time_record.place( x=500, y=500)		

			root.mainloop()


def createOutputFile():
	global fout
	global fin
	fout= wave.open(outFile,"w")
	fout.setparams(fin.getparams())
	
data=[]
ampFactor=1
shiftFactor=1
def readFile(guiFrameNumber):
	global fin
	global data
        global finWidth	
 	global ampFactor
 	global shiftFactor
 	global scaleFactor
	global isReversal

	if guiFrameNumber==1:
		    print "READ 1"
		    inFile=fileNames['wave1']
		    ampFactor=amp_bar1.get()
		    shiftFactor=shift_bar1.get()
		    scaleFactor=scale_bar1.get()
		    isReversal=var_reversal1.get()
	if guiFrameNumber==2:
		    print "READ 2"
		    inFile=fileNames['wave2']
		    ampFactor=amp_bar2.get()
		    shiftFactor=shift_bar2.get()
		    scaleFactor=scale_bar2.get()
		    isReversal=var_reversal2.get()
	if guiFrameNumber==3:
		    print "READ 3"
		    inFile=fileNames['wave3']
		    ampFactor=amp_bar3.get()
		    shiftFactor=shift_bar3.get()
		    scaleFactor=scale_bar3.get()
		    isReversal=var_reversal3.get()
	
	
        
	fin = wave.open(inFile, 'rb')
	type_channel = fin.getnchannels()
        sample_rate = fin.getframerate()
        finWidth = fin.getsampwidth()
        num_frames = fin.getnframes()
     
        raw_data = fin.readframes(num_frames ) # Returns byte data
        fin.close()
     
                    ## Unpacking of raw_Data to Integer Data
     
        num_samples = num_frames * type_channel
     
        if finWidth == 1:
                    fmt = "%iB" % num_samples # read unsigned chars
        elif finWidth == 2:
                    fmt = "%ih" % num_samples # read signed 2 byte shorts
        else:
                    raise ValueError("Only supports 8 and 16 bit audio formats.")
        formated_data = list(struct.unpack(fmt,raw_data))
        data=formated_data

def timeScaling(factor):
                a=[]
  		global fin
		global data             
                if(factor == 0):
                        factor=1
               	type_channel = fin.getnchannels()
                sample_rate = fin.getframerate()
                finWidth = fin.getsampwidth()
                num_frames = fin.getnframes()

                if type_channel == 1: 
                        k=int(len(data)/factor)
                        for i in range(k):
                                a.append(data[int(factor*i) ])
                else:
                        e_li=[]
                        o_li=[]
                        for i in range( len(data) ):
                                if(i%2 == 0):
                                        e_li.append(data[i])
                                else:
                                        o_li.append(data[i])
                        k=int(len(e_li)/factor)
                        for i in range(k):
                                a.append(e_li[ int(factor*i) ])
                                a.append(o_li[ int(factor*i) ])
               
                data = a
               	
"""	
def timeScaling(scaleFactor):
		temp=[]
		if scaleFactor>=1:
			for i in xrange(len(data)):
				data[i]=data[scaleFactor*i];
		else:
			for i in xrange(len(data)):
				temp[i]=data[i];
			for i in xrange(len(data)/)


"""		
		
def timeReversal():
                global data
		temp=[]
		for i in range(len(data)-1,0,-1):
                        temp.append(data[i])
		data=temp


def timeShifting(shiftFactor):    
                global data
		inp=shiftFactor*fin.getframerate()
		j=0
		inp=int(inp)
		
		if(inp>0):
			a=[]
			for i in range(inp):
				a.append(0)
			data=a+data
			
			
		else:
			inp=inp*-1
			data=data[inp:len(data)]


def record():
	chunk=1024
	
	global time_record
	
	FORMAT=pyaudio.paInt16
	channelsit=1
	some_rate=44100
	arr=[]
	record_seconds=int(time_record.get())	
	print 'seconds recording ' + str(record_seconds)
	p=pyaudio.PyAudio()
	stream1=p.open(format=FORMAT, channels=channelsit,rate=some_rate,input=True,output=True,frames_per_buffer=chunk)
	for i in range(0,44100/chunk*record_seconds):
		d=stream1.read(chunk)
		arr.append(d)
	wf=wave.open("output.wav",'wb')
	
	wf.setframerate(some_rate)	
	wf.setnchannels(channelsit)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	
	wf.writeframes(b''.join(arr))
	wf.close()
	stream1.stop_stream()
	stream1.close()
	p.terminate()

def ampScaling(ampFactor):    
 		global data
                for i in xrange(len(data)):
                        if data[i] * ampFactor > SHRT_MAX:
                                data[i] = SHRT_MAX
                        elif data[i] * ampFactor < SHRT_MIN:
                               data[i] = SHRT_MIN
                        else:
                                data[i] = data[i] * ampFactor
       
def pack_file():
		global data
		type_channel = fin.getnchannels()
                sample_rate = fin.getframerate()
                finWidth = fin.getsampwidth()
                num_frames = fin.getnframes()

                if finWidth==1:
                        fmt="%iB" % num_frames*type_channel
                else:
                        fmt="%ih" % num_frames*type_channel
 
                out_data=struct.pack(str(len(data))+"h",*(data))
		createOutputFile()
 		"""
                fout=wave.open("output_file.wav",'w')
 
                out_music_file.setframerate(self.sample_rate)
                out_music_file.setnframes(self.num_frames)
                out_music_file.setsampwidth(self.sample_width)
                out_music_file.setnchannels(self.type_channel)
                
 		"""
		fout.writeframes(out_data)                
		fout.close()

def askopenfile(frameNumber):
		if frameNumber==1:
	        	fileNames['wave1']=tkFileDialog.askopenfile(mode='rb',title='Choose a file')
			print fileNames['wave1']
			fileNames['wave1']=str(fileNames['wave1']).split('\'')[1]
			var1.set((str(fileNames['wave1']).split('/')[-1]).split('\'')[0])
			# root.update_idletasks()
		if frameNumber==2:
	        	fileNames['wave2']=tkFileDialog.askopenfile(mode='rb',title='Choose a file')
			print fileNames['wave2']
			fileNames['wave2']=str(fileNames['wave2']).split('\'')[1]
			var2.set((str(fileNames['wave2']).split('/')[-1]).split('\'')[0])

		if frameNumber==3:
	        	fileNames['wave3']=tkFileDialog.askopenfile(mode='rb',title='Choose a file')
			print fileNames['wave3']
			fileNames['wave3']=str(fileNames['wave3']).split('\'')[1]
			var3.set((str(fileNames['wave3']).split('/')[-1]).split('\'')[0])




def main():
		global wf
		global stream
	
		"""	
			# wait for stream to finish (5)
			#	while stream.is_active():
			
			#  	time.sleep(0.1)
			stream.stop_stream()
	
	
			
			# cleanup stuff.
			stream.close()   
			wf.close()
			p.terminate()	

		"""	
		createWidgets()


if __name__=="__main__":
	main()
