const crypto = require('crypto');

function getSecureString(length) {
    const characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
    const charLen = characters.length;

    // Generate random bytes
    const randomBytes = crypto.randomBytes(length);
    let result = '';

    for (let i = 0; i < length; i++) {
        // Use each byte value to select a character from the allowed set
        const idx = randomBytes[i] % charLen;
        result += characters.charAt(idx);
    }

    return result;
}

const result = getSecureString(10);
console.log(result);