// Utility functions: deep-merge, safe accessors, defaults chain loader

// deep-merge(a, b): recursive dictionary merge
// b wins for scalar values; recurse for nested dictionaries
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

// get(dict, key, default: ""): safe key access with fallback
#let get(dict, key, default: "") = {
  dict.at(key, default: default)
}

// get-nested(dict, keys, default: ""): nested access via key array
// Example: get-nested(data, ("contact", "email"), default: "N/A")
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

// load-defaults(values-file): load + merge YAML defaults chain
// Merges: contractor.yaml → federal.yaml → client.yaml (if exists) → values-file
// Client yaml path is passed via --input client-yaml=... by build.sh when the file exists
#let load-defaults(values-file) = {
  let layers = (
    yaml("/engagements/defaults/contractor.yaml"),
    yaml("/engagements/defaults/federal.yaml"),
  )

  // Client defaults: build.sh only passes client-yaml input when the file exists
  let client-path = sys.inputs.at("client-yaml", default: none)
  let layers = if client-path != none {
    (..layers, yaml("/" + client-path))
  } else {
    layers
  }

  let layers = (..layers, yaml("/" + values-file))
  layers.fold((:), deep-merge)
}
