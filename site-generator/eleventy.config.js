module.exports = function(eleventyConfig) {
	eleventyConfig.addPassthroughCopy("./style.css");
	eleventyConfig.addWatchTarget("./style.css");

	eleventyConfig.addLiquidShortcode(
		"nav_bar",
		/// active: String, buttons: (Display: String, Path: String)
		/// The active parameter should equval one Path in buttons
		function(...buttons) {

			let result = "<div id =\"nav-bar\"> <ul>";
			let active = this.page.filePathStem;
			console.log(buttons);

			for (let i = 0; i < buttons.length / 2; i++) {
				let name = buttons[2 * i];
				let path = buttons[2 * i + 1];

				result += "<li><a href=\"" + path + "\"";
				if (active === path) { // Find "active" tab
					result += " class=\"active\"";
				}
				result += ">" + name + "</a></li>";
			}
			result += "</ul></div>";
			return result;
		}
	);

	return {
		dir: {
			input: "site",
			output: "../"
		}
	}
};
