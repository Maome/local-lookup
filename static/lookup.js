document.addEventListener('paste', handlePaste);

function handlePaste (e) {
    var clipboardData, pastedData;

    // Stop data actually being pasted into div
    e.stopPropagation();
    e.preventDefault();

    // Get pasted data via clipboard API
    clipboardData = e.clipboardData || window.clipboardData;
    pastedData = clipboardData.getData('Text');

    // Do whatever with pasteddata
    goToCharacters(pastedData);
}


function goToCharacters(text) {
    var characterString = getCommaSeparatedCharacters(text)
    if(characterString != "") {
        window.location = "/characters/" + characterString;
    }
}

function getCommaSeparatedCharacters(inputText) {
    var characters = ""
    var lines = inputText.split('\n');
    for(var i = 0;i < lines.length;i++){
        if(lines[i].trim().length > 0) {
            if(characters != "") {
                characters += ","
            }
            console.log(lines[i].trim())
            characters += lines[i].trim()
        }
    }
    return characters
}
