$(document).ready(function () {
	const max = [5, 3, 5, 5, 10, 5, 1, 5, 2, 5, 5, 27, 8, 2, 2, 5, 4, 4, 3, 5, 4, 5, 5, 4, 6, 2, 5, 5, 2, 3, 5, 4, 5, 6, 2, 4, 2, 10, 6, 5, 5, 5, 5, 4, 5, 2, 4, 2, 5, 2, 5, 3, 5, 5, 7, 2, 5, 2, 2, 5, 2, 4, 6, 8, 7, 2, 7, 5, 5, 2, 3, 5, 5, 2, 1, 5, 2, 3, 3, 8, 5, 4, 3, 2, 5, 2, 10, 5, 5, 5, 4, 6, 5, 10, 5, 5, 5, 5, 3, 2, 5, 4, 5, 5, 5, 5, 2, 3, 4, 3, 5, 5, 4, 2, 5, 9, 2, 2, 5, 2, 4, 4, 2, 4, 5, 1, 5, 5, 5, 2, 5, 5, 5, 14, 2, 1, 3, 5, 10, 9, 2, 2, 2, 2, 5, 2, 2, 5, 5, 5, 12, 5, 2, 5, 5, 6, 5, 5, 5, 5, 4, 9, 5, 2, 2, 5, 2, 5, 2, 2, 2, 5, 5, 5, 5, 2, 2, 4, 2, 2, 7, 5, 2, 9, 2, 5, 5, 5, 4, 2, 7, 5, 5, 5, 4, 5, 5, 2, 7, 5, 5, 5, 5, 5, 5, 2, 2, 2, 5, 2, 3, 2, 5, 3, 6, 2, 2, 7, 5, 5, 5, 10, 2, 2, 5, 5, 2, 1, 10, 5];

	$("#number_subject, #range_subject").on('change input', changeSubjectHandler);

	function changeSubjectHandler() {
		let subject = parseInt(params.subject);
		let subjectsMax = max[subject - 1];
		$("#number_trial, #range_trial").attr({ "max": subjectsMax });
		$("#maxmin-1 > span:nth-child(1)").html("Max: " + subjectsMax);
		if (parseInt(params.trial) >= subjectsMax) $("#number_trial, #range_trial").val(subjectsMax);
		params.trial = $("#range_trial").val();
	}

	$("#number_trial, #range_trial").on('change input', function () {
		let subject = parseInt(params.subject);
		let subjectsMax = max[subject - 1];
		if (parseInt(params.trial) >= subjectsMax) $("#number_trial, #range_trial").val(subjectsMax);
	});
});
