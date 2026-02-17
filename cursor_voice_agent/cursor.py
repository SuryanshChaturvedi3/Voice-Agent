import speech_recognition as sr
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

import asyncio
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer

openai = AsyncOpenAI()

async def tts(speech):
    async with openai.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="coral",
        input=speech,
        instructions="Speak in a cheerful and positive tone.",
        response_format="pcm",
    ) as response:
         await LocalAudioPlayer().play(response)


client = OpenAI()
async def main():
    r = sr.Recognizer()  
    
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            r.pause_threshold = 2

            SYSTEM_PROMPT = f"""
               you are an expert voice agent. You are given the transcript of what
               user has said using voice.
               you need to output as if you are an voice agent and whatever you speak
                will be convertd back to audio using AI and played back to user.
                """
            messages = [{"role":"system", "content":SYSTEM_PROMPT}]
     
            while True:
                print("Speak Something....")
                audio = r.listen(source)

                print("Processing Audio...(STT)")
                stt = r.recognize_google(audio)  # type: ignore

                print("You said:", stt)
                
                messages.append({"role":"user", "content":stt})
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages
                )
                
                print("AI Response:",response.choices[0].message.content)
                await tts(speech=response.choices[0].message.content)
                
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
    except sr.UnknownValueError:
        print("Could not understand audio")
    except Exception as e:
        print(f"An error occurred: {e}")

asyncio.run(main())
 
