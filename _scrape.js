function DL() {
var filename = "MENU__"+document.title.split(' - ')[0].replace(/ /g, '-')+'.json';
var data = [...document.querySelectorAll('.menuSection.undefined')].map(_s => ({
sectionTitle: _s.querySelector('.menuSection-title').innerText,
itemNames: [..._s.querySelectorAll(".menuItemNew-name")].map(e => e.innerText),
itemPrices: [..._s.querySelectorAll(".menuItem-displayPrice")].map(e => e.innerText),
itemDescriptions: [..._s.querySelectorAll(".menuItemNew-description--truncate")].map(e => e.innerText),
}))
var a = document.createElement("a");
var file = new Blob([JSON.stringify(data)], {type: 'text/json'});
a.href = URL.createObjectURL(file);
a.download = filename;
a.click()
}