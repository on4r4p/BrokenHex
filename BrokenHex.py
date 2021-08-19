#!/usr/bin/python3

from argparse import ArgumentParser
import os,sys,urllib.request,shutil

def GetNewSample(source):

       response = urllib.request.urlopen(source)
       data = response.read()
       return(data)


def HexDiff(orig,new):
   print("\nLooking for occurences between in both samples.")
   h=0
   x=2
   while True:
       if orig[h:x] == new[h:x]:
          Rebuild_File(orig[h:x],h,x)
       h = h+2
       x = x+2
       if x >= Matching_Goal:
           break
   print("\nDone searching for occurences inside those samples.\n")

def Rebuild_File(hex,start,end):
     global File_Result

     print("\nFound %s at offset %d to %d "%(hex,start,end))
     print("Saving to File_Result...\n")
     File_Result[start:end] = hex
     return




parser = ArgumentParser()
parser.add_argument("-u","--Url",dest="Source_Sample",help="Url to sample",default=None,metavar="Url")
Args = parser.parse_args()


if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)

if Args.Source_Sample is None:
    print("Please fillup an url to download sample.\n")
    parser.print_help(sys.stderr)
    sys.exit(1)
else:
     Source_Sample = Args.Source_Sample


Original_Sample_Name = "./HexSample"


File_Result = []


if os.path.isfile(Original_Sample_Name) is True:

    with open(Original_Sample_Name, 'rb') as f:
        Original_Sample = f.read().hex()
else:

    with urllib.request.urlopen(Source_Sample) as response, open(Original_Sample_Name, 'wb') as Sample_Out:
         shutil.copyfileobj(response, Sample_Out)
    with open(Original_Sample_Name, 'rb') as f:
         Original_Sample = f.read().hex()

print("Original_Sample Loaded.")
print("Number of char in Original_Sample :",len(Original_Sample))
print("\nSetting Matching_Goal to :",len(Original_Sample))

Matching_Goal = len(Original_Sample)
for i in range(Matching_Goal):
    File_Result.append(".")

print("\nLoading New Sample in memory.")
New_Sample=GetNewSample(Source_Sample).hex()
print("New_Sample Loaded.")
print("Number of char in New_Sample :",len(New_Sample))

if len(New_Sample) == len(Original_Sample):
   print("\nNumber of char in both sample are equal.\nGood to go.")
   HexDiff(Original_Sample,New_Sample) 


print("File_result is now :\n\n","".join(File_Result))
