function getDomUpdateFn(varName, scope){
  return function (value){
    const domElements = document.querySelectorAll(`[data-tie*='${scope}.${varName}']`)
    for(var j=0; j < domElements.length; ++j){
      const ties = (domElements[j].getAttribute('data-tie') || '')
        .split(' ')
        .filter(function (tie){
          return tie != '' && tie.endsWith(`:${scope}.${varName}`)
        })
      for(var i=0; i < ties.length; ++i){
        let [prop, vname] = ties[i].split(':')
        vname = vname.slice(`${scope}:`.length)
        switch(prop){
          case 'value':
            domElements[j].value = value;
            break;
          case 'innerHTML':
            domElements[j].innerHTML = value;
            break;
          default:
            domElements[j].setAttribute(prop, value)
        }
      }
    }
  }
}

function bindToDom(scope, obj){
  const keys = Object.keys(obj)
  let access = {}  // add get/set methods here
  let store = {}  // actually store the information needed
  let listeners = {}  // to update dependencies when data changes
  let recordEvents = false
  let events = []
  for(var i=0; i < keys.length; ++i){
    const varName = keys[i]
    if(typeof(obj[varName]) !== 'function'){
      // When var is set, update DOM
      access[varName] = {
        get: function (){
          if(recordEvents === true){
            events.push({op: 'get', key: varName})
          }
          return store[varName]
        },
        set: function (value){
          getDomUpdateFn(varName, scope)(value)
          store[varName] = value
          const toCall = listeners[varName]
          if(toCall !== undefined){
            let fnKeys = Object.keys(toCall)
            for(j = 0; j < fnKeys.length; ++j){
              const fk = fnKeys[j]
              const fn = toCall[fk]
              obj[fk] = fn(obj)
            }
          }
        },
      }
      // set value in store
      access[varName].set(obj[varName])
      // When DOM changes, update var by adding event listeners
      document.addEventListener('change', function(e){
        if(
          e.target
          && (e.target.getAttribute('data-tie') || '').indexOf(`value:${scope}.${varName}`) !== -1
        ) { obj[varName] = e.target.value }
      })
    }  // when key is not function 
  }  // loop
  obj = Object.defineProperties(obj, access);
  // Add events for functions
  for(i=0; i < keys.length; ++i){
    const varName = keys[i]
    if(typeof(obj[varName]) === 'function'){
      events = []
      recordEvents = true
      let initValue = obj[varName](obj)
      for(j = 0; j < events.length; ++j){
        const dependency = events[j].key
        if(!(dependency in listeners)){
          listeners[dependency] = {}
        }
        if(!(varName in listeners[dependency])){
          listeners[dependency][varName] = obj[varName]
        }
      }
      access[varName] = {
        get: function (){
          if(recordEvents === true){
            events.push({op: 'get', key: varName})
          }
          return store[varName] 
        },
        set: function (value){
          getDomUpdateFn(varName, scope)(value)
          store[varName] = value
          const toCall = listeners[varName]
          if(toCall !== undefined){
            let fnKeys = Object.keys(toCall)
            for(j = 0; j < fnKeys.length; ++j){
              const fk = fnKeys[j]
              const fn = toCall[fk]
              obj[fk] = fn(obj)
            }
          }
        },
      }
      access[varName].set(initValue)
      obj = Object.defineProperties(obj, access);
    }  // when key is not function 
  }  // loop
  events = []
  recordEvents = false
  return obj
}
