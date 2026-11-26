/* Contact form enhancement. Without JS the form still works: it posts to a
   mailto: address with enctype text/plain. With JS we build a cleaner email
   (subject + readable body) and open it with the user's mail app. */
(function () {
  var form = document.getElementById("contact-form");
  if (!form) return;
  var status = document.getElementById("form-status");
  var TO = "colin@swyft-hq.com";

  function val(name) {
    var el = form.elements[name];
    if (!el) return "";
    if (el.length && !el.tagName) {
      for (var i = 0; i < el.length; i++) if (el[i].checked) return el[i].value;
      return "";
    }
    return (el.value || "").trim();
  }

  form.addEventListener("submit", function (e) {
    if (!form.checkValidity()) return;
    e.preventDefault();
    var role = val("role") || "Not sure";
    var business = val("business");
    var subject = "Swyft Business Broker inquiry: " + role + (business ? " (" + business + ")" : "");
    var body = [
      "Name: " + val("name"),
      "Business name: " + (business || "-"),
      "Email: " + val("email"),
      "Phone: " + (val("phone") || "-"),
      "I am a: " + role,
      "",
      "Message:",
      val("message")
    ].join("\n");
    window.location.href = "mailto:" + TO + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
    if (status) {
      status.textContent = "Your email app should open with this message filled in. If it does not, email " + TO + " or call 267-606-8667.";
    }
  });
})();
