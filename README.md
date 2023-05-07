# Folder Cleaner
#### Video Demo:  https://youtu.be/eQVR0Cpt2ss
#### Description:
My program simply cleans up a folder on your system. Currently, it only cleans the downloads folder, but in the future I want to find how to allow the user to choose what directory to organize. However, I currently set it to just the downloads because I wanted to automate it to clean my own downloads every hour using Windows task scheduler.

In order to clean up the Downloads directory, Folder Cleaner does 3 things:
1. Find and delete duplicate files
2. Sort files into folders based on file type
3. Delete unused directories

I'll explain my design decisions for each process.

### 1. Find and Delete Duplicate Files
I frequently download books, instructions, forms, and a lot of other junk. Sometimes, I love my junk so much that I forget I downloaded it and (thinking I'll finally read it this time) download it again. As such, I have a ton of exact duplicates in my downloads folder and they're not always easy to find. So, here's how we find the duplicates:
1. Make a dictionary of all the files' sizes (sizes are keys)
2. List out the names of all the files at each size (names are a list of values)
3. See if any file names have the same base name (using regex...)
4. Send the copies to the trash bin

I chose to add an external dependency and include the "send2trash" library. I considered using the shutil library, but the send2trash library works on all operating systems (or a lot more than I can implement with my current knowledge) in case I want to make this cross platform later. Python only has native support for permanently deleting files as far as I could tell. So, send2trash allows me to store the files in the trash bin in case something important accidently gets moved.

I also had to use regular expressions to check for duplicates. To be honest, I really didn't want to because I'm always scared that the regex I made will give me false positives or negatives. I tested my regex on the website [regextester](https://www.regextester.com/) extensively with many different file names. It seems okay, but only time will tell. I also only have Windows systems to test on, so I don't know if Linux or Mac has the same naming convention for copies. I suspect at least Mac is different, so I might need to implement a system check or create a whole new program for Mac if I want to go down that route.

Finally, I made the choice to not remove user-duplicated files (ones that have "Copy" appended to them). This is because I often make these on purpose so I can keep an original and a modified copy. Usually these will be different file sizes, but just in case they end up with the same file size, I didn't want to delete any user created copies.

#### UPDATE!
I changed from the os library to pathlib to simplify some code and make it a little more readble. This reduced the length of the code by about 20 lines and sped it up, although minimally. According to documentation, pathlib is also better at working cross platform making it more portable (but I'm sure there are other things I need to fix first to achieve that).

### 2. Sort Files Into Folders Based On File Type
Honestly, this is the one I started with. I thought, "Hey, it would be much easier to clean up these 300 files if they were in labelled folders!" Maybe _now_ they will since I don't have to look at 300 files. Here was my process for sorting files:
1. Get the extension of a file
2. Check if that extension has a folder
3. IF that folder extists, set it as the target
- Otherwise make that folder and set it as the target
- (NOTE: I originally made all the folders first and then cleaned them up later, but I thought making them only when needed would be better design.)
4. Finally, move the file
- IF there's an ERROR, print the error and skip to the next file

Because this was my first time working with moving files around, I originally chose to stop the program in case of errors because this was originally the whole point of this program and if a file can't be moved, I'd rather figure out why immediately (inadequate permissions, folder names changed, incorrect path, etc.) rather than have it possibly mis-sort something. Even though I tested it pretty thoroughly, I'm still worried about losing files, but it didn't make sense to end the program when it could just try to move the next file. I know it __can__ work properly, so I'm going to trust that it __will__ work properly.

### 3. Delete Unused Directories
This could be mostly a _me_ problem. I have a habit of moving things out of folders they were downloaded in (think zip files) and then not cleaning up the empty folder. I wanted to get those husks out of my life. But, I also realized that because of this habit, if I move some files out of the downloads folder, I might be left with a lot of unused folders that __this program__ created! I don't want an empty __Disks__ folder sitting around for no reason. So, that's where "kill_folders" comes in. This is definitely the simplest one, and it was a good chance to practice recursion:
1. Find all folders (and subfolders) in Downloads
2. Check if that (sub)folder has any files
3. If it's empty, delete it forever. Don't even send it to the bin.
- If it has folders inside it, call kill_folders again

So, I was being very careful with not deleting files forever, but with empty folders, I just wanted to nuke them out of existence. I originally was using send2trash again, but an empty folder doesn't have useful information that I could lose. That said, if I ever make this for other people to use, I would make this a tick-box that they could disable.

### TESTING with PYTEST
This was where the real struggle happened. Because my program doesn't return any values, I had to figure out how to make test files to work with, and then check that those test files were in the right place. This worked fine, but the problem arose with hidden system files again, namely *desktop.ini* in the Downloads folder. I worked around this by making a *test_dir* to do my testing in, but then my file sorting function didn't work. So, I had to let my file sorting funtion work in the main downloads and everything else work in the test folder (since everything else was checking how many files existed after running and hidden files messed with my count). Then, I switched to pathlib... and everyting broke. I literally had to remake my pytest files all over. But, now my program passes all the tests, and it helped me catch some bugs.

I  mean, I learned a lot about testing. For example, if you nest a function that works with system file paths inside another function, and run a test on the parent function, you best believe that something can go wrong if you change directories for testing.

And I did catch some bugs, namely that directories that contained empty directories were not deleted after they became empty themselves. I fixed this and was able to use recursion to make it a little more elegant. So, mission accomplished. Thanks pathlib!

### Reflections
I did make this program over multiple days, and development didn't always go in order. I was making different functions in different files as I was learning and then tried to put them all into the "folder_cleaner.py" that you see today. So, some of my working files are pretty different from the final production.

I tried to optimize where I could, for example if I needed a list for multiple functions, I tried to call it just once. I thought about moving files out of user-made folders, but I sometimes organize on my own, and I don't want to mess up that organization. I tried to use as few outside libraries as possible in case I wanted to move this to another computer (fewer libraries means fewer changes, I hope). I also thought about putting two of my three main functions in the same loop, but I wanted to keep them seperate in case I don't want to run one of them later (like an options check box).

One optimization that I couldn't figure out how to implement was sending duplicate files to the bin immediately, instead of adding them to the dictionary first. Since I wanted to keep the originals and delete the copies, I needed to create the whole dictionary first because searching for which one is the copy. It seems like it should be simple, but my brain just isn't having it. So, for now this works and I'll leave it.

Overall, I'm happy with what I made because, well, I made it! I learned A LOT about the os, shutil, and pathlib libraries while researching what is best for my use case. And pathlib finally helped object oriented programming click in my head. This is my first program that I designed, and it runs how I wanted it to do on my system at least.

### Wish List
There are some things that I might want in the future. I thought about including them now, but I couldn't decide if it's best for them to live in the same program or make specialized ones. Anyway, here's what I would want if I update my code:
1. be able to change the monitored directory
2. automatically move files into other system directories (e.g. ~/Documents, ~/Music)
3. group certain files together when it makes sense (e.g. when a movie and subtitle file should be together)
4. customize which types of files to look for (e.g. don't organize archives, just delete)
5. compare duplicates by contents of the file, not just size and name