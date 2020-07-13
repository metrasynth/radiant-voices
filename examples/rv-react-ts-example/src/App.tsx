import React, { useCallback, useState } from "react"
import { useDropzone } from "react-dropzone"
import * as sunvox from "./sunvox-lib-loader"

import "./App.css"
import {
  Pattern,
  Project,
  fromIffBuffer,
  m,
  projectChunks,
  readSunVoxFile,
  toIffBuffer,
} from "radiant-voices"
import FileSaver from "file-saver"

function App() {
  const [alsoDownload, setAlsoDownload] = useState(false)
  const toggleAlsoDownload = () => setAlsoDownload(!alsoDownload)
  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles.length > 0 && acceptedFiles[0].type === "audio/sunvox") {
      const acceptedFile = acceptedFiles[0]
      console.log(acceptedFile)
      const reader = new FileReader()
      reader.onload = () => {
        const buf = reader.result as ArrayBuffer
        const project = readSunVoxFile(fromIffBuffer(buf))
        console.log({ project })
        sunvox.sv_close_slot(0)
        sunvox.sv_open_slot(0)
        const arr = new Uint8Array(buf)
        sunvox.sv_load_from_memory(0, arr)
        sunvox.sv_play_from_beginning(0)
      }
      reader.readAsArrayBuffer(acceptedFile)
    }
  }, [])
  const onClick = () => {
    const project = new Project()
    project.initialBpm = 150
    const fm = m.fm().attachTo(project)
    fm.name = "FreqMod"
    project.outputModule.incomingLinks.push(fm.index)
    const pat = new Pattern(8, 1).attachTo(project)
    pat.data[0][0].note = 49
    pat.data[0][0].module = fm.index + 1
    pat.data[1][0].note = 128 // note off
    console.log({ project })
    sunvox.sv_close_slot(0)
    sunvox.sv_open_slot(0)
    for (const chunk of projectChunks(project)) {
      console.log(chunk)
    }
    const file = new Uint8Array(toIffBuffer(projectChunks(project)).buffer)
    if (alsoDownload) {
      const blob = new Blob([file], { type: "application/octet-stream" })
      FileSaver.saveAs(blob, "fromWebBrowser.sunvox")
    }
    console.log({ file })
    console.log(sunvox.sv_load_from_memory(0, file))
    sunvox.sv_play_from_beginning(0)
    ;(window as any).sunvox = sunvox
  }
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
      <div>
        <input
          type="checkbox"
          id="alsoDownload"
          onChange={toggleAlsoDownload}
          checked={alsoDownload}
        />
        <label htmlFor="alsoDownload">Also download</label>
      </div>
      <div>
        <button onClick={onClick}>
          Click me to generate a radiant-voices project!
        </button>
      </div>
    </div>
  )
}

export default App
