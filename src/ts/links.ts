export interface Linkable {
  linkFrom(other: Linkable | Linkable[]): Linkable
  linkTo(other: Linkable | Linkable[]): Linkable
}

export class Linkables implements Linkable {
  members: Linkable[]
  constructor(members: Linkable[]) {
    this.members = members
  }
  linkFrom(other: Linkable | Linkable[]): Linkable {
    const o = new Linkables(other instanceof Array ? other : [other])
    for (const linkable of o.members) {
      linkable.linkTo(this)
    }
    return o
  }
  linkTo(other: Linkable | Linkable[]): Linkable {
    const o = new Linkables(other instanceof Array ? other : [other])
    for (const linkable of o.members) {
      linkable.linkFrom(this)
    }
    return o
  }
}
