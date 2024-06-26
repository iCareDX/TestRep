import { Log } from "~/logger"

const _selectEngine = (mode: string) => {
  if (mode === "whisper") {
    return require("./speech-to-text-whisper")
  } else if (mode === "browser") {
    return require("./speech-to-text-browser")
  } else if (mode === "reazon") {
    return require("./speech-to-text-reazon")
  } else if (mode === "vosk") {
    return require("./speech-to-text-VOSK")
  } else if (mode === "google") {
    // return require("./speech-to-text-google-old")
    return require("./speech-to-text-google")
  }
  return require("./speech-to-text-disabled")
}

export const selectEngine = (mode: string) => {
  return _selectEngine(mode).default()
}

////////////////////////////////////////////////////////////////////////////////////////////////////////
// main
////////////////////////////////////////////////////////////////////////////////////////////////////////

function main() {
  const speech = selectEngine("vosk").default
  Log.info(speech)
}

if (require.main === module) {
  main()
}
