const dorm_path = '/dormitory/agreement';
const query_path = '/dormitory/agreement-query-fixme';

function currentIsDormPage() {
    var current_url = window.location.pathname;
    return current_url.includes(dorm_path);
}

function getAgreementState() {
    return fetch(query_path)
        .then(response => response.json())
        .then(data => {
            // Bad design:
            // If user do not have to sign,
            // or user has signed, return is not empty.
            return data.length > 0;
        })
        .catch(error => {
            console.error('Error fetching agreement state:', error);
            return true; // Pretend user has signed on network error.
        });
}

$(function() {
    if (!currentIsDormPage()) {
        getAgreementState().then(signed => {
            if (!signed) {
                window.location.href = dorm_path;
            }
        });
    }
});
