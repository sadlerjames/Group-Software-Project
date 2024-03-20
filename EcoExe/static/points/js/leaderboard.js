// Authored by Jack Hales

var leaderboardType = 'treasure_hunt'

function showTreasureHunts() {
    leaderboardType = 'treasure_hunt';
    var filterOptions = document.getElementsByClassName('filter-options');
    for (var i = 0; i < filterOptions.length; i++) {
        filterOptions[i].hidden = true;
    }
    loadOptions();
    displayData();
}

function showQuizzes() {
    leaderboardType = 'quiz';
    var filterOptions = document.getElementsByClassName('filter-options');
    for (var i = 0; i < filterOptions.length; i++) {
        filterOptions[i].hidden = false;
    }
    loadOptions();
    displayData();
}

// Function to display the data from the database
function displayData() {
    var option = $('#leaderboard-options').find('option:selected').attr('leaderboard');
    var filter_option = $('#filter-options').find('option:selected').attr('filter');
    if (option && filter_option) {
        $.ajax({
            url: '/points/get_points',
            data: { 
                "quiz_id": option,
                "filter": filter_option,
                "type": leaderboardType
            },
            type: 'GET',
            dataType: 'json',
            success: function(data) {
                // Clear existing table rows
                $('#points-table-body').empty();
                $('#user-rank').empty();
                user_rank_set = false
                is_data = false
                // Iterate through each user and append to table
                $.each(data, function(index, point) {
                    rank = parseInt(index) + 1
                    $('#points-table-body').append(
                        '<tr>' +
                        '<td>' + rank + '</td>' +
                        '<td>' + point.username + '</td>' +
                        '<td>' + point.points + '</td>' +
                        '</tr>'
                    );
                    is_data = true
                    // Show logged in user rank
                    if (point.username == username) {
                        $('#user-rank').append('You are currently ranked ' + rank + ' with ' + point.points + ' points!')
                        user_rank_set = true
                    }
                });
                if (is_data == false) {
                    $('#points-table-body').append(
                        '<tr>' +
                        '<td></td>' +
                        '<td>No rankings available</td>' +
                        '<td></td>' +
                        '</tr>'
                    );
                }
                if (user_rank_set == false) {
                    $('#user-rank').append('You currently have no ranking for this leaderboard!')
                }
            },
            error: function(xhr, status, error) {
                console.error('Failed to fetch points data:', status, error);
            }
        });
    }
}

// Function to fetch options from server and populate dropdown
function loadOptions() {
    $.ajax({
        url: '/points/fetch_options',
        type: 'GET',
        data: {
            "type": leaderboardType
        },
        dataType: 'json',
        success: function(options) {
        var dropdown = $('#leaderboard-options');
        dropdown.empty()
        dropdown.append($('<option>').text('Overall Leaderboard').attr('leaderboard', 'overall')); 
        // Iterate through each option and append to dropdown
        $.each(options, function(index, value) {
            if (leaderboardType == 'treasure_hunt') {
                dropdown.append($('<option>').text('Treasure Hunt: ' + value.quiz_name).attr('leaderboard', value.quiz_id));    
            } else if (leaderboardType == 'quiz') {
                dropdown.append($('<option>').text('Quiz: ' + value.quiz_name).attr('leaderboard', value.quiz_id));
            }
        });
        },
        error: function(xhr, status, error) {
            console.error(error);
            $('#ajax-response').html('Error occurred while fetching options.');
        }
    });

}

$(document).ready(function(){
    // Set click listeners
    $('#btnTreasureHunt').on('click', showTreasureHunts);
    $('#btnQuizzes').on('click', showQuizzes);
    var filterOptions = document.getElementsByClassName('filter-options');
    for (var i = 0; i < filterOptions.length; i++) {
        filterOptions[i].hidden = true;
    }

    // Load options
    loadOptions();
    
    // Event listener for dropdown change
    $('.dropdown').change(function(){
        displayData();
    });

    // Perform AJAX request on page load to fetch points data from server for first dropdown option
    displayData();
});