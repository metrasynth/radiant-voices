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
import { randomProject } from "./randomProject"

interface AppOptions {
  initialProject?: Project | string
  initialFile?: Uint8Array
  initialFilename?: string
}

function App({ initialProject, initialFile, initialFilename }: AppOptions) {
  const [file, setFile] = useState(initialFile)
  const [filename, setFilename] = useState(initialFilename)
  const [project, setProject] = useState(initialProject)

  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles.length > 0 && acceptedFiles[0].type === "audio/sunvox") {
      const acceptedFile = acceptedFiles[0]
      console.log(acceptedFile)
      setFilename(acceptedFile.name)
      const reader = new FileReader()
      reader.onload = () => {
        const buf = reader.result as ArrayBuffer
        const newProject = readSunVoxFile(fromIffBuffer(buf))
        if (!(newProject instanceof Project)) {
          setProject("Not a SunVox project")
          return
        }
        setProject(newProject)
        console.log({ newProject })
        sunvox.sv_close_slot(0)
        sunvox.sv_open_slot(0)
        const arr = new Uint8Array(buf)
        setFile(arr)
        sunvox.sv_load_from_memory(0, arr)
        sunvox.sv_play_from_beginning(0)
      }
      reader.readAsArrayBuffer(acceptedFile)
    }
  }, [])
  const onGenerateClick = () => {
    const { project, filename } = randomProject()
    setProject(project)
    setFilename(filename)
    console.log({ project })
    sunvox.sv_close_slot(0)
    sunvox.sv_open_slot(0)
    for (const chunk of projectChunks(project)) {
      console.log(chunk)
    }
    const file = new Uint8Array(toIffBuffer(projectChunks(project)).buffer)
    setFile(file)
    console.log({ file })
    console.log(sunvox.sv_load_from_memory(0, file))
    sunvox.sv_play_from_beginning(0)
    ;(window as any).sunvox = sunvox
  }
  const onDownloadClick = () => {
    if (!file) return
    const blobParts = [file]
    const options = { type: "application/octet-stream" }
    const blob = new Blob(blobParts, options)
    FileSaver.saveAs(blob, filename)
  }
  const onPlayClick = () => {
    sunvox.sv_play_from_beginning(0)
  }
  const onStopClick = () => {
    sunvox.sv_stop(0)
  }

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop })

  return (
    <div className="App">
      <h1>sunvox.audio</h1>
      <h2>What is this?</h2>
      <p>
        This is an early, work-in-progress demonstration of the SunVox and Radiant
        Voices libraries for JavaScript.
      </p>
      <h3>Project loader</h3>
      <p>
        Load a SunVox project (*.sunvox file) from your computer, and it will play it
        back in SunVox and load the project in Radiant Voices:
      </p>
      <div {...getRootProps()} className="DropZone">
        <input {...getInputProps()} />
        {isDragActive ? (
          <p>Drop the files here</p>
        ) : (
          <p>Drag 'n' drop files here, or click to select files</p>
        )}
      </div>
      <h3>Project generator</h3>
      <p>
        This is a proof-of-concept project generator that creates a pseudo-random SunVox
        project based on your inputs.
      </p>
      <button onClick={onGenerateClick}>
        Click me to generate a radiant-voices project!
      </button>
      <h3>Project inspector</h3>
      <button onClick={onDownloadClick} disabled={!project}>
        Download the currently-playing project
      </button>
      &nbsp;
      <button onClick={onPlayClick} disabled={!project}>
        Play
      </button>
      &nbsp;
      <button onClick={onStopClick} disabled={!project}>
        Stop
      </button>
      <p>
        Whether you load a project or generate one, here's what some if it looks like
        from Radiant Voice's perspective:
      </p>
      {!(project instanceof Project) ? (
        <p>(No project loaded)</p>
      ) : (
        <div>
          <p>Project name: {project.name}</p>
          <p>Filename: {filename}</p>
          <p>Patterns: {project.patterns.filter((x) => x).length}</p>
          <p>Modules: {project.modules.filter((x) => x).length}</p>
        </div>
      )}
    </div>
  )
}

export default App
