from google.cloud import texttospeech
import datetime


default_voice = 1

def chose_a_voice ():
    # List of options
    options = ["Option 1: Play audio", "Option 2: Record audio", "Option 3: Save file", "Option 4: Exit"]

    # Display options to the user
    print("Please choose from the following options:")

    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")

    # Prompt the user for input
    user_choice = input("Enter the number of your choice: ")

    # Check if the input is valid and map the choice
    try:
        choice_index = int(user_choice) - 1  # Convert input to an index
        if 0 <= choice_index < len(options):
            selected_option = options[choice_index]
            print(f"You chose: {selected_option}")
        else:
            print("Invalid choice. Please select a valid number.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def generate_audio_file_name():
    now = datetime.datetime.now()

    # Example format: YYYY-MM-DD_HH-MM-SS
    return now.strftime("audio_%Y-%m-%d_%H-%M-%S")


def read_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def text_to_speech(text, output_audio_file):
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set up the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Set the voice parameters for Russian Wavenet male voice D
    voice = texttospeech.VoiceSelectionParams(
        language_code="ru-RU",                # Russian language code
        name="ru-RU-Wavenet-D",               # Specific voice
        ssml_gender=texttospeech.SsmlVoiceGender.MALE
    )

    # Set the audio config as per your request
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16,  # LINEAR16 format for WAV output
        effects_profile_id=["headphone-class-device"],       # Effects profile for headphones
        pitch=0,                                             # Default pitch
        speaking_rate=1                                      # Normal speaking rate
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # Write the output to a file
    with open(output_audio_file, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to "{output_audio_file}"')



def list_voices():
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Performs the list voices request
    voices = client.list_voices()

    # Display the available voices
    print("Available voices:")
    for voice in voices.voices:
        language_codes = ", ".join(voice.language_codes)
        name = voice.name
        ssml_gender = texttospeech.SsmlVoiceGender(voice.ssml_gender).name
        natural_sample_rate_hz = voice.natural_sample_rate_hertz
        print(f"Name: {name}")
        print(f"Supported languages: {language_codes}")
        print(f"SSML Gender: {ssml_gender}")
        print(f"Sample Rate: {natural_sample_rate_hz} Hz")
        print("-" * 40)

# if __name__ == "__main__":
#     list_voices()        

if __name__ == "__main__":

    audio_file_name = generate_audio_file_name()

    message = f"Enter audio file name (default - {audio_file_name} ): "
    audio_file_user_input = input(message)

    if audio_file_user_input:
        audio_file_name = audio_file_user_input

    print(f"ITS {audio_file_name}!")

    #CHOOSE SOURCE TEXT FILE
    text_file_path = "text.txt"
    
    text_content = read_text_from_file(text_file_path)
    
    # CHANGE THE OUTPUT FILE NAME
    text_to_speech(text_content, f"{audio_file_name}.mp3")