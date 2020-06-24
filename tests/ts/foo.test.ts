import { foo } from "../../src/ts"

test("value of foo", () => {
  expect(foo).toBe(12)
})
