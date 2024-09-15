import os
from dotenv import load_dotenv
from langchain_community.document_loaders import AssemblyAIAudioTranscriptLoader
import assemblyai as aai
import yt_dlp
from langchain_upstage import UpstageEmbeddings

load_dotenv()

ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")

# aai.settings.api_key = ASSEMBLYAI_API_KEY
# transcriber = aai.Transcriber()

# transcript = transcriber.transcribe("https://storage.googleapis.com/aai-web-samples/news.mp4")
# # transcript = transcriber.transcribe("./my-local-audio-file.wav")

# print(transcript.text)


# 1. Download Podcast
def download_podcast(url, output_path='downloads/podcast'):
    # Ensure the output path is within the current working directory
    output_path = os.path.join(os.getcwd(), output_path)
    
    # yt-dlp options for downloading the podcast
    ydl_opts = {
        'format': 'bestaudio/best',  # Best available audio quality
        'outtmpl': output_path,      # Output filename
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',  # Extract only audio
            'preferredcodec': 'mp3',      # Convert to mp3 format
            'preferredquality': '192',    # Quality of the audio
        }],
    }

    # Download the podcast using yt-dlp
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Example usage
# podcast_url = "https://music.youtube.com/watch?v=3n3RRGBl0bs&si=S303lRMLUhLiKzuf"
# download_podcast(podcast_url)


# 1.1 - Load Podcast URL
podcast_local_path = "downloads/podcast.mp3"

config = aai.TranscriptionConfig(
    speaker_labels=True, 
    auto_chapters=True, 
    entity_detection=True
)

loader = AssemblyAIAudioTranscriptLoader(
    file_path=podcast_local_path,
    api_key=ASSEMBLYAI_API_KEY,
    config=config
)
docs_load = loader.load()
docs = docs_load[0].page_content


# 2. Create Embeddings

upstage_embeddings = UpstageEmbeddings(
    api_key="UPSTAGE_API_KEY",
    model="solar-embedding-1-large"
)

embeddings = upstage_embeddings.embed_documents(docs)

# 3. Store in Vector Database



def main():
    print("Ok. Done!!!")
    #print(docs)
    print(doc_result)
    #print(query_result)








if __name__ == "__main__":
    main()