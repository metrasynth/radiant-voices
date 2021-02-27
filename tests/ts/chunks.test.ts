import { Project } from "../../src/ts"
import { toIffBuffer } from "../../src/ts/chunks/toIffBuffer"
import { fromIffBuffer } from "../../src/ts/chunks/fromIffBuffer"
import { objectChunks } from "../../src/ts/writer/objectChunks"

const emptyProject = new Project()
const emptyChunks = Array.from(objectChunks(emptyProject))

describe("chunks of an empty Project", () => {
  test("starts with SVOX", () => {
    const chunk = emptyChunks[0]
    expect(chunk).toEqual({ name: "SVOX", type: "empty" })
  })
})

describe("saving and loading an empty Project", () => {
  test("is the same after loading", () => {
    const outbuf = toIffBuffer(objectChunks(emptyProject))
    const chunks2 = Array.from(fromIffBuffer(outbuf))
    expect(emptyChunks).toEqual(chunks2)
  })
})
