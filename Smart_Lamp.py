#!/usr/bin/env python

from tkinter import *
from tkinter import simpledialog, messagebox
import gpiozero
import time
import threading

"""Tkinter Initialization"""
main = Tk()
main.title('Smart Lamp')
main.geometry('370x220')
main.resizable(width=FALSE, height=FALSE)

"""Raspberry Initialization"""
ldrpin = 27
pirpin = 4
relaypin = 17
times = 30
lightvalue = 5
ldr = gpiozero.LightSensor(ldrpin) #Memanggil class MotionSensor dari Library gpiozero
pir =  gpiozero.MotionSensor(pirpin) #Memanggil class MotionSensor dari Library gpiozero
relay1 = gpiozero.OutputDevice(relaypin, active_high=False, initial_value=False) #set relay sebagai OutputDevice
 
        
def time_sett():
    global times
    times = simpledialog.askinteger("TIME (s)", "Enter Time (in second)",initialvalue=times,minvalue=4)
    while times == None:
        messagebox.showwarning(message='Time tidak boleh kosong')
        times = simpledialog.askinteger("TIME (s)", "Enter Time (in second)",initialvalue=times,minvalue=4)

    
def light_sett():
    global lightvalue
    lightvalue = simpledialog.askinteger("Light Value", "Masukan Intensitas Cahaya\nUntuk Mengaktifkan Lampu\n(1 - 10) 1 = Gelap 10 = Terang",initialvalue=lightvalue,minvalue=1, maxvalue=10)
    while lightvalue == None:
        messagebox.showwarning(message='Light Value tidak\nboleh kosong')
        lightvalue = simpledialog.askinteger("Light Value", "Masukan Intensitas Cahaya\nUntuk Mengaktifkan Lampu\n(1 - 10) 1 = Gelap 10 = Terang",initialvalue=lightvalue,minvalue=1, maxvalue=10)


#fungsi untuk mengatur berapa lama lampu akan menyala dari terakhir kali mendeteksi gerakan
def countdown(times):
    while (pir.value == 1): #pir.value = 1 berarti sensor mendeteksi gerakan
        relay1.on()#menyalakan relay
        labelOn.configure(image=gc1)
        labelOff.configure(image=rc0)
        while times > 0:
            times -= 1
            time.sleep(1)
        relay1.off() #mematikan relay
        labelOn.configure(image=gc0)
        labelOff.configure(image=rc1)
        
#fungsi untuk mengkonversi waktu yang nantinya digunakan untuk menghitung berapa lama
#lampu dalam keadaan hidup
def time_convert(sec):
  mins = sec // 60
  sec = sec % 60
  hours = mins // 60
  mins = mins % 60
  print("Time Lapsed = {0}:{1}:{2}".format(int(hours),int(mins),sec))
        

def Slamp():
    #global ldr,pir,relay1
    try:
        while True:
            value = float("%.3f" % ldr.value)*10
            label2.configure(text=value)
            if pir.value == 0:
                label3.configure(text="Motion UnDetected")
            else:
                label3.configure(text="Motion Detected")
            print(value)#print nilai resistensi LDR
            if (value < lightvalue): #0 = gelap
                print("Ligth UnDetected")
                pir.wait_for_motion(timeout=1) #menunggu adanya gerakan(waktu tunggu 3 detik)
                if pir.motion_detected:
                    label3.configure(text="Motion Detected")
                    print("Motion Detected")
                    start_time = time.time() #awal perhitungan waktu
                    countdown(times) #lama waktu 5 detik
                    end_time = time.time() #mengakhiri perhitungan waktu
                    time_lapsed = int(end_time) - int(start_time) #menghitung lamanya waktu lampu hidup
                    time_convert(time_lapsed)#konversi waktu dalam satuan jam:menit:detik
            if (value >= lightvalue): #1 = terang
                print("Ligth Detected")
                pir.wait_for_motion(timeout=1)
                if pir.motion_detected: #kondisi jika mendeteksi gerakan
                    label3.configure(text="Motion Detected But Theres Light")
                    print("Motion Detected But Theres Light")
                    time.sleep(1)
                #label3.configure(text="Motion UnDetected")    
                #print("Motion UnDetected")
            if stop == 1:
                break
            
    except KeyboardInterrupt:
        pass
    
def start():
# Assign global variable and initialize value
    global stop
    stop = 0
    button2.config(state=NORMAL)
    button1.config(state=DISABLED)
    # Create and launch a thread 
    t = threading.Thread(target = Slamp)
    t.start()

def stop():
    # Assign global variable and set value to stop
    global stop
    stop = 1
    button1.config(state=NORMAL)
    button2.config(state=DISABLED)

        
"""Program Interface"""
label1 = Label(main, text="STATUS")
label1.grid(column=0, row=0, columnspan=2,padx=10, pady=10)

#Gambar Lampu hidup
gc0 = PhotoImage(file='gc0.png')
gc1 = PhotoImage(file='gc1.png')
labelOn = Label(main, image=gc0)
labelOn.grid(column=0, row=1)

#Gambar Lampu mati
rc0 = PhotoImage(file='rc0.png')
rc1 = PhotoImage(file='rc1.png')
labelOff = Label(main, image=rc1)
labelOff.grid(column=1, row=1)

#Tombol Start
button1 = Button(main, text='START', command=start)
button1.grid(row=4, column=0, columnspan=2,sticky=W+E,padx=5, pady=5)
button1.grid_propagate(0)

#Tombol Stop
button2 = Button(main, text='STOP', command=stop)
button2.grid(row=5, column=0, columnspan=2,sticky=W+E,padx=5, pady=5)
button2.grid_propagate(0)

"""LDR STATUS"""
#Frame LDR status
frame1 = LabelFrame(main, text="LDR Value",height=50 , width=250,relief=GROOVE,borderwidth=1)
frame1.grid(row=0, column=2, rowspan=3,padx=10, pady=10,sticky=W+E)
frame1.grid_propagate(0)
#label inside frame1
label2 = Label(frame1)
label2.grid(row=2, column=0, sticky=W+E)
label2.grid_propagate(0)

"""PIR STATUS"""
#Frame PIR status
frame2 = LabelFrame(main, text="PIR Status", height=50 , width=250,relief=GROOVE,borderwidth=1)
frame2.grid(row=2, column=2, rowspan=3,padx=10, pady=10,sticky=W+E )
frame2.grid_propagate(0)
#label inside frame2
label3 = Label(frame2)
label3.grid(row=0, column=0, sticky=W+E)
label3.grid_propagate(0)

"""Light & Time Settings"""
#Frame Light and Time Settings
frame3 = LabelFrame(main, text="Settings", height=70 , width=270,relief=GROOVE,borderwidth=1)
frame3.grid(row=5, column=2, rowspan=3,padx=10, pady=10,sticky=W+E )
frame3.grid_propagate(0)

#Tombol Light
button4 = Button(frame3, text='Light', command=light_sett)
button4.grid(row=0, column=0,padx=5, pady=5)
button4.grid_propagate(0)

#Tombol Time
button5 = Button(frame3, text='Time', command=time_sett)
button5.grid(row=0, column=1,padx=5, pady=5)
button5.grid_propagate(0)


main.mainloop()


