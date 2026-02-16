#let deep-merge(a, b) = {
  let result = a
  for (key, val) in b {
    if key in result and type(result.at(key)) == dictionary and type(val) == dictionary {
      result.insert(key, deep-merge(result.at(key), val))
    } else {
      result.insert(key, val)
    }
  }
  result
}

#let get(dict, key, default: "") = {
  dict.at(key, default: default)
}

#let get-nested(dict, keys, default: "") = {
  let current = dict
  for key in keys {
    if type(current) == dictionary and key in current {
      current = current.at(key)
    } else {
      return default
    }
  }
  current
}

#let render-lines(s) = {
  if type(s) != str { return s }
  s.trim().split("\n").join(linebreak())
}
