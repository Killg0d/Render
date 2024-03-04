document.querySelector(".jsFilter").addEventListener("click", function () {
  document.querySelector(".filter-menu").classList.toggle("active");
});

document.querySelector(".grid").addEventListener("click", function () {
  document.querySelector(".list").classList.remove("active");
  document.querySelector(".grid").classList.add("active");
  document.querySelector(".products-area-wrapper").classList.add("gridView");
  document
    .querySelector(".products-area-wrapper")
    .classList.remove("tableView");
});

document.querySelector(".list").addEventListener("click", function () {
  document.querySelector(".list").classList.add("active");
  document.querySelector(".grid").classList.remove("active");
  document.querySelector(".products-area-wrapper").classList.remove("gridView");
  document.querySelector(".products-area-wrapper").classList.add("tableView");
});

var modeSwitch = document.querySelector('.mode-switch');
modeSwitch.addEventListener('click', function () {                      
document.documentElement.classList.toggle('light');
 modeSwitch.classList.toggle('active');
});

var descriptions = document.querySelectorAll('.description');
var readMoreLinks = document.querySelectorAll('.read-more');

var maxLength = 10; // Maximum length of the description to be displayed

for (var i = 0; i < descriptions.length; i++) {
  var description = descriptions[i];
  var readMoreLink = readMoreLinks[i];

  // Truncate the description and add an ellipsis
  var fullText = description.textContent;
  var truncatedText = fullText.substring(0, maxLength).trim();
  description.textContent = truncatedText;

  // Show/hide the full description when the "Read more" link is clicked
  readMoreLink.addEventListener('click', createToggleHandler(description, truncatedText, fullText));
}

function createToggleHandler(description, truncatedText, fullText) {
  return function (event) {
    event.preventDefault();
    if (description.classList.contains('collapsed')) {
      description.textContent = truncatedText;
      description.classList.remove('collapsed');
      event.target.textContent = '...';
    } else {
      description.textContent = fullText;
      description.classList.add('collapsed');
      event.target.textContent = '<-';
    }
  };
}
