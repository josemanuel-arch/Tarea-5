# Video script (English) · Activity 4: Melate in Java

**Hard limit: 3 minutes, .mp4 format.** Target: about 2 minutes 30 seconds.
Short sentences on purpose, so they are easy to say out loud.

## How we will build the video (two separate recordings)

1. **Record the screen first, with no voice.** Follow the actions column
   below, in order, at a calm pace. Leave 2 or 3 seconds of "nothing"
   between sections. Windows: Win+G (Game Bar) or PowerPoint screen
   recording. Mac: Cmd+Shift+5.
2. **Then record the audio.** Play back your screen recording and narrate
   over it while you watch, reading the script below. Use your phone's
   voice recorder or the PC microphone. Watching the playback keeps your
   voice in sync with what happens on screen.
3. **Send me both files** here in the chat: the screen video (.mp4 or .mov)
   and the audio (.m4a or .mp3). I will merge them, trim them, and return
   the final .mp4 under 3 minutes.

## Script

**[Screen: Melate.java open in the editor] (0:00 – 0:20)**

"Hello, my name is José Manuel Rodríguez Cantú, student ID 00612676.
This is my Activity 4 for Module 4 of Object Oriented Programming.
The program generates the 7 winning numbers for the Melate lottery game.
The numbers go from 1 to 56, and they cannot be repeated."

**[Screen: scroll slowly through the code] (0:20 – 1:10)**

"Let me walk you through the code. In the method generarNumeros, I use
the Random class from the java util package. This is part of the Java
Standard Library. The method nextInt of 56 returns a number from 0 to 55,
so I add 1 to get a number between 1 and 56.

I store the numbers in a collection: an ArrayList called numberList.
Before adding each number, I use the contains method to check that the
number is not duplicated. If it is already in the list, the program
generates a new one.

Then, in the method guardarNumeros, I save the list in a persistent
medium: a text file called melate dot txt. For this I use the FileWriter
and PrintWriter classes. All of this is inside a try catch block that
handles the IOException, so the program does not crash if the file
cannot be opened."

**[Screen: terminal — run `javac Melate.java`, then `java Melate` twice, then open melate.txt] (1:10 – 2:00)**

"Now let's run it. I compile with javac, and I run it with java Melate.
Here is the output: the program prints the 7 winning numbers. All of them
are between 1 and 56, and none of them is repeated.

I run it a second time. The numbers are different, because they are
random. But again: exactly 7 numbers, and no duplicates.

Finally, I open the file melate dot txt. Here are the numbers from the
last run, saved in the text file. This is the evidence that the
persistence works."

**[Screen: back to the code, or the output] (2:00 – 2:30)**

"To conclude, in this activity I used four things from Java. Collections:
the ArrayList makes it very easy to store the numbers and check for
duplicates with contains. The Standard Library: the Random class for the
random numbers. Persistence: FileWriter and PrintWriter to save the
results in a text file. And exception handling: the try catch block
prevents the program from failing if the file cannot be opened. With
this, the system meets all the requirements of the activity. Thank you."

## Tips for the audio

- Speak slowly. Short pauses are fine; I can cut silence when I edit.
- If you make a mistake, do not stop the recording: pause, and repeat the
  whole sentence. I will cut the bad take.
- Record in a quiet room, phone close to your mouth.

## What I need from you

1. The screen recording (no voice needed).
2. The audio recording.
3. I will return the final .mp4, maximum 3 minutes, ready to upload to
   Brightspace together with Melate.java and Melate.class.
