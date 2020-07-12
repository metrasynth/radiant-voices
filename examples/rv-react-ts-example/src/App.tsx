import React, { useCallback } from "react"
import { useDropzone } from "react-dropzone"
import * as sunvox from "./sunvox-lib-loader"

import logo from "./logo.svg"
import "./App.css"
import { readSunVoxFile } from "radiant-voices"
import { fromIffBuffer } from "radiant-voices"

function App() {
  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles.length > 0 && acceptedFiles[0].type === "audio/sunvox") {
      const acceptedFile = acceptedFiles[0]
      console.log(acceptedFile)
      const reader = new FileReader()
      reader.onload = () => {
        const buf = reader.result as ArrayBuffer
        const project = readSunVoxFile(fromIffBuffer(buf))
        console.log({ project })
        sunvox.sv_open_slot(0)
        const arr = new Uint8Array(buf)
        sunvox.sv_load_from_memory(0, arr)
        sunvox.sv_play_from_beginning(0)
      }
      reader.readAsArrayBuffer(acceptedFile)
    }
  }, [])
  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop })
  return (
    <div className="App">
      <div {...getRootProps()}>
        <input {...getInputProps()} />
        <p>&nbsp;</p>
        <p>&nbsp;</p>
        <p>&nbsp;</p>
        {isDragActive ? (
          <p>Drop the files here</p>
        ) : (
          <p>Drag 'n' drop files here, or click to select files</p>
        )}
        <p>&nbsp;</p>
        <p>&nbsp;</p>
        <p>&nbsp;</p>
      </div>
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.tsx</code> and save to reload.
        </p>
      </header>
    </div>
  )
}

export default App
