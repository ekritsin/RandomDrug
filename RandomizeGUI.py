from tkinter import *
from tkinter import messagebox
from tkinter import filedialog  
import os.path
import errno
import random
import itertools
import re
import webbrowser



class RandomizeApp:
    
    def __init__(self, master):
        '''Initialize GUI window '''
        random.seed()   
               
        frame = Frame(master)
        frame.pack()
        
        master.title('Randomization List Generator')
        
        #------------Menu       
        self.displayMenu(master)
        
        #-----------Welcome Message Frame
        welcome = Frame(master)
        welcome.pack(side= TOP)
        
        self.message = ''' Welcome to the 3:3:2 Randomization Program\n
        ----- Test drug : Reference drug : Placebo -----\nPlease select one of the following randomization methods'''
        self.msg = Message(welcome, text = self.message)
        self.msg.config(bg='white', font=('arial', 10),width = 450)
        self.msg.pack(side=TOP,padx=5,pady=5,fill=X)
        
        #-----------Buttons Frame
        buttons = Frame(master)
        buttons.pack()
        
        self.b = Button(buttons, text="Simple Randomization", command=self.create_windowA)
        self.b.pack( padx=5, pady=5,fill=X)
                
        self.s = Button(buttons, text="Block Randomization", command=self.create_windowB)
        self.s.pack( padx=5, pady=5,fill=X)
                
        self.d = Button(buttons, text="Stratified Randomization", command=self.create_windowC)
        self.d.pack(padx=5, pady=5,fill=X)
        
        #--------Photo
        photo_frame = Frame(master)
        photo_frame.pack()
        
        self.photo = PhotoImage(file="random.png")
        self.ph = Label(photo_frame, image=self.photo)
        self.ph.pack(padx=5 ,pady=5)
        
    def displayMenu(self,master):
        ''' Defines MENU for frames'''
        self.menu = Menu(master)
        master.config(menu = self.menu)      
          
        appMenu = Menu(self.menu)
        self.menu.add_cascade(label='Application', menu=appMenu)
        appMenu.add_command(label='Go to Current Results',command=self.goTo)
        appMenu.add_separator()
        appMenu.add_command(label='Exit', command=master.quit)    
         
        helpMenu = Menu(self.menu)       
        self.menu.add_cascade(label='Help', menu = helpMenu)
        helpMenu.add_command(label='Guidelines',command=self.instructions)
        helpMenu.add_command(label='About', command= self.about)
        
        
        
    def about(self):
        messagebox.showinfo("Title", "Project by Ermioni Kritsinioti\nMSc Biomath ") 
    def goTo(self):
        
        
        try:
            if os.path.exists(self.folder_path):
                webbrowser.open(self.folder_path)
                
        except AttributeError:
            self.noFileError()
            
    def instructions(self):
        ''' Instructions for the three randomization methods  '''
        self.newWindow = Toplevel()
         
        
        self.message = '''Randomization as a method of experimental control has been extensively used in human clinical trials and other biological experiments.
        It prevents the selection bias and insures against the accidental bias. 
        It produces the comparable groups and eliminates the source of bias in treatment assignments
        
        Simple Randomization: Randomization based on a single sequence of random assignments. In order to maintain a 3:3:2 ratio for Raference Drug:Test Drug:Placebo , users are only allowed to enter candidate numbers that are multiple of 7 and preferably have a sample size that is above 21.
        
        Block Randomization: The block randomization method is designed to randomize subjects into groups that result in equal sample sizes. This method is used to ensure a balance in sample size across groups over time. Block sizes are chosen randomly for each group in numbers 7,14 or 21 and ratio 3:2:2 is kept between all blocks.
        
        Stratified Randomization: The stratified randomization method addresses the need to control and balance the influence of covariates. This method can be used to achieve balance among groups in terms of subjects baseline characteristics (covariates). Specific covariates must be identified by the researcher who understands the potential influence each covariate has on the dependent variable.
        Stratified randomization is achieved by generating a separate block for each combination of covariates or strata, and subjects are assigned to the appropriate block of covariates. After all subjects have been identified and assigned into blocks, simple randomization is performed within each block to assign subjects to one of the groups.
        Note that in order to perform stratification , user needs to enter a candidate number that is a multiple of 28. Factors should not be more than 4-5 in order to have coverage for all stratas. For example if users need 2 covariates/factors like Age:under 30 years,over 30 years and Weight:Under 60 kgs,over 60kgs, our stratas will equal to 2x2 = 4 sratifications. 
        Therefore Strata 1 is under 30 years/under 60kgs, strata 2 is under 30 years/over 60kgs, strata 3 is over 30 years/over 60 kgs and strata 4 is over 30 years /over 60kgs. '''
        self.instructs = Message(self.newWindow, text = self.message) 
        self.instructs.config(bg='lightgrey', font=('arial', 10),width = 450)
        self.instructs.pack(side=TOP,padx=5,pady=5,fill=X)
    def fetch(self,entries):
        ''' Function to get entries.Takes a list input from getEnts '''
        self.texts = []
        for entry in entries:
            field = entry[0]
             
            text  = entry[1].get()
             
            self.texts.append(text)
            print('%s: "%s"' % (field, text)) 
            entry[1].config(state = 'disabled') 
        return self.texts
     
    def makeform(self,master, fields):
        ''' Function that makes fields and entries for each method. Takes fields for input '''
        self.entries = []
        
        
        for field in fields:
            row = Frame(master)
            lab = Label(row, width=15, text=field, anchor='e')
            ent = Entry(row)
            ent.focus()
            row.pack(side=TOP, fill=X, padx=5, pady=5)
            lab.pack(side=LEFT)
            ent.pack(side=RIGHT, expand=YES, fill=X)
            self.entries.append((field, ent))
        
        return self.entries
 
    def getEnts(self):
        
        self.entries_list = self.fetch(self.ents)
        return self.entries_list
    def saveFile(self):
        
        self.filename =  filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("txt files","*.txt"),("all files","*.*")))
        return self.filename
    def showStatus(self):
        
        self.newWindow.lift()
        status = Label(self.newWindow, text='Results saved in {}'.format(self.folder_path),bd=1,relief=SUNKEN,anchor = W)
        status.pack(side=BOTTOM, fill=X)
        status.after(3000, lambda: status.destroy())#close status after 3secs
        return None
###################################  Simple  ######################
    def Simple(self,n):
        #treatments = ['test_drug' ,'ref_drug','placebo']
        treatA = int(round(n*3./8)) # separating the size of each group (ratios 3:2:2)
        treatB = int(round(n*3./8))
        treatC = int(round(n*2./8))
        print('Test Drug: {} Reference Drug: {} Placebo: {} \n'.format(treatA,treatB,treatC))
        
        self.population = ['Test Drug']*treatA + ['Reference Drug']*treatB + ['Placebo']*treatC
        random.shuffle(self.population)                   
        #print(self.population)
        
        return self.population
    
    def writeFileSimple(self,results):
        '''Takes a list as input and creates a file and a folder if it does not exist '''
        #homepath = os.getenv('USERPROFILE')        
        #folder_path = os.path.join(homepath+'\Desktop\Randomize_App\\resultSimple.txt')
        
        self.folder_path = self.saveFile()+'.txt'
        print(self.folder_path)

        try:
            if not os.path.exists(self.folder_path):
                with open(self.folder_path,'w') as wf:
                                    
                                    for index,item in enumerate(results, start=1):
                                        items = 'Candidate {} is assigned to the {} treatment.'.format(index,item)
                                        wf.write("%s\n" % items)
                wf.close()
                self.showStatus()
            else:
                messagebox.showerror('Error', 'File name already exists!')
                self.newWindow.lift()
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                    raise
            
    
    def simpleRand(self):
        self.b1.configure(state = DISABLED)#disables button 
        patients = int(self.getEnts()[0])
        
        if patients<8 or patients%8!=0:
            self.intError()
        else:
            s_list = self.Simple(patients)   
            self.writeFileSimple(s_list)

        return None
    
    def create_windowA(self):
        ''' Creates window and fields for the simple randomization '''
        print('A clicked')
        fields = ['Candidate Number']
        self.newWindow = Toplevel()        
        self.displayMenu(self.newWindow)       
         
        self.ents = self.makeform(self.newWindow, fields)
        self.newWindow.bind('<Return>', self.getEnts)   
        self.b1 = Button(self.newWindow,text = 'Now randomize',command= self.simpleRand)        
        self.b1.pack(side=TOP, padx=5, pady=5)
        
        
################################Blocked  ###########################################    
    def writeFileBlock(self,results):
        '''takes a 2 - dimensional list and writes a file for Block randomization '''
        self.folder_path = self.saveFile()+'.txt'
        print(self.folder_path)

        try:
            if not os.path.exists(self.folder_path):
                with open(self.folder_path,'w') as wf:
                            
                            for index,item in enumerate(results, start=1):
                                items = 'Block {}:'.format(index)
                                wf.write("%s\n" % items)
                                for i,drug in enumerate(item,start=1):
                                    result = 'Candidate {} is assigned to the {} treatment.'.format(i,drug)
                                    wf.write("%s\n" % result)
                wf.close()
                self.showStatus()
            else:
                messagebox.showerror('Error', 'File name already exists!')
                self.newWindow.lift()
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                    raise
        
    def Blocked(self,n):
        blocks_list = []
        blocks = 1
        temp_block_size = 8
        while n:
            
            #temp_block_size = random.choice([7,14,21])     #random block size selection                        
            
            if temp_block_size>n:
                temp_block_size = n
                #print("Corrected")
                    
            n = n - temp_block_size  
            print("----- Block {} with block size {} ----- \n".format(blocks,temp_block_size))
            x_block = self.Simple(temp_block_size)
            blocks_list.append(x_block)
            blocks +=1
        
        #print(blocks_list)
        return blocks_list
    
    def blockRand(self):
        self.b1.configure(state = DISABLED)
        patients = int(self.getEnts()[0])
        
        if patients<8 or patients%8!=0:
            self.intError()
        else:
            b_list = self.Blocked(patients)
            self.writeFileBlock(b_list)
            
        return None
    
    def create_windowB(self):         
        print('B clicked')
        fields = ['Candidate Number']
        self.newWindow = Toplevel()#new window pops up
        self.displayMenu(self.newWindow)   
        
        self.ents = self.makeform(self.newWindow, fields)
        self.newWindow.bind('<Return>', self.getEnts)   
        self.b1 = Button(self.newWindow,text = 'Now randomize', command = self.blockRand)
        self.b1.pack(side=TOP, padx=10, pady=10)
######################################Sratification ##################################       
    def writeFileStrata(self,results,factors,levels):
        #results is a 3d list of stratas and blocks , factors is a string ,levels is a list of the paired stratas
        self.folder_path = self.saveFile()+'.txt'
        print(self.folder_path)

        try:
            if not os.path.exists(self.folder_path):
                with open(self.folder_path,'w') as wf:            
                    for index,item in enumerate(results, start=1):
                        current_level = ",".join(levels[index-1])
                        items = '----------- Strata {} : {} ------\n-----------Factors: {}'.format(index,current_level,factors)
                        wf.write("%s\n" % items)
                        for i,drugs in enumerate(item,start=1):
                            cur_block = '--- Block {}'.format(i)
                            wf.write("%s\n" % cur_block)
                            for j,drug in enumerate(drugs,start=1):
                                result = 'Candidate {} is assigned to the {} treatment.'.format(j,drug)
                                wf.write("%s\n" % result)
                wf.close()
                self.showStatus()
            else:
                messagebox.showerror('Error', 'File name already exists!')
                self.newWindow.lift()
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                    raise
        
    def strataRand(self):
        n = self.patients
        self.b2.configure(state = DISABLED)
        #self.b2.destroy()
        levels = []
        
        strata = 1
        factors = self.getEnts()
        for factor in factors:
            pattern = re.compile(r'(.+):(.+),(.+)')
            matches = pattern.search(factor)
            if not matches:
                self.patternError()
        
        for i in range(len(factors)):
            level = factors[i].split(':')[1].split(',')
            levels.append(level)
            strata *= len(level)
        
        levels = list(itertools.product(*levels))
        print('Levels is {} and strata is {}'.format(levels,strata))
        
        try:
            strata_size = int(n/strata) #separate candidates into stratas
            assert(strata_size >= 8),'Small sample size!'
            factors = ' - '.join(factors)
            strata_results = []
            i=0
            while i!=strata:
            
                print("Factors: ",factors)
                ##For every strata we make a blocked randomization with random sized blocks
                current_level = ",".join(levels[i])
                print("Strata {}: {}".format(i+1,current_level))
                print("=================================")
                res = self.Blocked(strata_size)
                strata_results.append(res)
                i+=1
            print(strata_results)
            

            if i==strata:
                self.writeFileStrata(strata_results,factors,levels)
   
        except AssertionError as a:
            print('Too small sample size for {} stratifications !'.format(strata),a)
            self.overflowError(strata)

    def getFactors(self):
        ''' get factors for stratification '''
        self.b1.destroy()        
        try:
            self.patients = int(self.getEnts()[0])
            factors = int(self.getEnts()[1])
            assert(self.patients>8 and self.patients%32==0),'Multiple of 32 please!'
            
            msg = Label(self.newWindow,text="For example 'Age:under 30 years, over 30 years'")
            msg.pack(padx=5,pady=5)
            fields = ["Factor"]*factors
           
            self.ents = self.makeform(self.newWindow, fields)
            self.newWindow.bind('<Return>', self.getEnts)
            self.b2 = Button(self.newWindow,text='Get Results',command= self.strataRand)
            self.b2.pack(padx=10, pady=10) 
            
        except AssertionError as e:
            print(e)
            self.intError()            

        except ValueError:
            self.intError1()
            
        return None
    
    def create_windowC(self):
        
        print('C clicked')
        fields = ['Candidate Number','Factors']
        self.newWindow = Toplevel()
        self.displayMenu(self.newWindow)
        
        strata_message = Label(self.newWindow, text = 'Please make sure that your sample is a multiple of 32...')
        strata_message.pack(side=TOP, padx=10, pady=10)
        
        self.ents = self.makeform(self.newWindow, fields)
        self.newWindow.bind('<Return>', self.getEnts)   
        self.b1 = Button(self.newWindow,text = 'Define Factors', command = self.getFactors)
        self.b1.pack(side=TOP, padx=10, pady=10)
########################################## Errors      
        
    def intError(self):
        messagebox.showerror("Error", "Candidate number should be multiple of 8!")
        self.newWindow.destroy()
    def intError1(self):
        messagebox.showerror("Error", "Input should be integers only!")
        self.newWindow.destroy()
    def overflowError(self,strata):
        messagebox.showerror("Error", "Too small sample size for {} stratifications ! Small sample size!".format(strata)) 
        self.newWindow.destroy()
    def noFileError(self):
        messagebox.showerror('Error', 'No such file or directory created')
    def patternError(self):
        messagebox.showerror("Error", "Wrong input pattern for the factors!\nPattern should match following: 'Age:under 30 years,over 30 years' etc.") 
        self.newWindow.destroy()
###########################################################################################
               
if __name__ == '__main__':
    root = Tk()    
    bye = RandomizeApp(root)
    
    
    root.mainloop()