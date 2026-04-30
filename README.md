🦾 JARVIS: My Hand-Built Voice Assistant-

"The smartest thing in my room (mostly)"
Hi! I'm a beginner developer, and this is JARVIS. I wanted a voice assistant like Tony Stark’ when i was a kid and i got interested in tech and coding becuase of JARVIS and Iron Man.So,making this thing did fulfill my small wish of having an JARVIS

Jarvis lives in my computer, listens to me, remembers things about me, and even uses a "Brain" (Gemini API) to talk back to me and can open some tabs like youtube and google.


🐢 The "Honest" Section -

Tbh Jarvis is kind of slow due to api stuff and i am a beginner so idk how to make it very fast. And sometime it also lags. I used the help of ai but it couldnt do any well.And there are some limitations like sometime speech recognition doesnt work as it should be and this JARVIS is only available to Windows


✨ What can JARVIS do?-

1.🎙️ Wake Word Detection: He wakes up when u say JARVIS

2.🧠 Brain: He uses Google’s Gemini 2.5 Flash Lite to answer questions and chat and you can use any model of your choice.

3.🔍 Web Search: You can search something and it will fetch the results and then our ai brain will summarise it for you. 

4.🌐 Web Control: He can open YouTube, Google, GitHub, or Slack and even open google and search anything you want.

5.💾 Two-Layer Memory: 
                     Short-Term: He remembers the last few things you said so the conversation flows.

                    Long-Term: He saves facts about you (like your name or birthday) in a "Diary" file so he never forgets.

6.🗣️ Persistent Voice: I built a special "PowerShell Pipe"(with ChatGpt help) as pyttsx3 was not working.


🚀 How it Works (The Simple Logic)-


1.Standby Mode: Jarvis listens for a loud spike in sound. If it sounds like "Jarvis," he says "Yes Sir!"

2.Active Listening: He watches your voice volume. When you stop talking, he "clips" that audio and turns it into text using numpy array.

3.The Router : Jarvis looks at your words and decides where to go:

    "Open YouTube" → Launch the Browser.

    "Search for..." → Go to the Web.

    "Who are you?" → Ask the AI Brain.

4.Memory Check: He checks if you told him something important to save in his JSON "Diary."

5.The Mouth: He sends the final answer to a hidden Windows tool(Powershell) to speak it out loud.


🛠️ The Lab Equipment (Tech Stack)

The Heart: Python 3.14+

The Ears: speech_recognition & sounddevice (No PyAudio—it kept breaking!)

The Brain: google-generativeai (Gemini 2.5 flash lite)

The Web-Searcher: ddgs (DuckDuckGo Search)

The Memory: json files (Your data stays on your computer!)

The Mouth: Windows PowerShell (System.Speech)


📁 The Project Files-

main.py: The main control center.

short_term.json: His "Post-it Notes" for the current chat.

long_term.json: His "Permanent Diary" for your name, birthday, and likes.

.env: The "Secret Vault" where your API keys stay safe and btw it is hidden bcs og .gitignore file



⚙️ Setup Instructions
1. Install the Python parts:

Use this command in ur terminal:
pip install speechrecognition sounddevice numpy python-dotenv google-generativeai duckduckgo_search

2. Add your Secret Keys:

Create a file called .env in the main folder and put your key inside:

Code snippet
GEMINI_API_KEY=your_key_here
SLACK_LINK=your_slack_link_here

3. Run the App:

Run this command on ur terinal:
python main.py

👶 Notes for Fellow begineer like me:

I wrote this code in a LEGO-brick style. I didn't make one giant, scary mess of code(I think so)Instead, I split it into small pieces: one for the ears, one for the brain, and one for the mouth. This makes it way easier to read and learn from!

Warning: If you have a quiet voice, you might need to change the loudness threshold in the code from 6500 to a smaller number like 2500.

🔮 Future Ideas

⚡ Faster wake-word detection.

🎨 A cool visual window (UI) so he’s not just a black box.

🏠 Controlling my actual room lights or music.

🤖 Where was AI used-

I took chatgpt and gemini help to figure out libraries commands and function as i am a begginer.I also made JARVIS mouth completely by JARVIS as pyaudio was not available for latest versions and i could not figure out anything.I used my creativity for the memory feature and many more things were done by me and some were done by AI

BYEE!