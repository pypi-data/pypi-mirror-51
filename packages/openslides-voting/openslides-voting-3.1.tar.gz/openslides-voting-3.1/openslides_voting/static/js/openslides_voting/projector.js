(function () {

'use strict';

angular.module('OpenSlidesApp.openslides_voting.projector', [
    'OpenSlidesApp.openslides_voting'
])

.config([
    'slidesProvider',
    function(slidesProvider) {
        slidesProvider.registerSlide('voting/prompt', {
            template: 'static/templates/openslides_voting/slide_prompt.html'
        });
        slidesProvider.registerSlide('voting/icon', {
            template: 'static/templates/openslides_voting/slide_icon.html'
        });
        slidesProvider.registerSlide('voting/motion-poll', {
            template: 'static/templates/openslides_voting/slide_motion_poll.html',
        });
        slidesProvider.registerSlide('voting/assignment-poll', {
            template: 'static/templates/openslides_voting/slide_assignment_poll.html',
        });
    }
])

.controller('SlidePromptCtrl', [
    '$scope',
    function($scope) {
        // Attention! Each object that is used here has to be dealt with on server side.
        // Add it to the corresponding get_requirements method of the ProjectorElement
        // class.
        $scope.message = $scope.element.message;
    }
])

.controller('SlideIconCtrl', [
    '$scope',
    function($scope) {
        // Attention! Each object that is used here has to be dealt with on server side.
        // Add it to the corresponding get_requirements method of the ProjectorElement
        // class.
        $scope.message = $scope.element.message;
        $scope.visible = $scope.element.visible;
    }
])

.controller('SlideMotionPollCtrl', [
    '$scope',
    '$timeout',
    'AuthorizedVoters',
    'Config',
    'Motion',
    'MotionPoll',
    'MotionPollBallot',
    'MotionPollDecimalPlaces',
    'User',
    'Delegate',
    'VotingController',
    function ($scope, $timeout, AuthorizedVoters, Config, Motion, MotionPoll,
              MotionPollBallot, MotionPollDecimalPlaces, User, Delegate, VotingController) {
        // Each DS resource used here must be yielded on server side in ProjectElement.get_requirements!
        var pollId = $scope.element.id,
            draw = false; // prevents redundant drawing

        $scope.$watch(function () {
            // MotionPoll watch implies Motion watch! So there is no need for an extra Motion watcher.
            return MotionPoll.lastModified(pollId);
        }, function () {
            $scope.poll = MotionPoll.get(pollId);
            if ($scope.poll !== undefined) {
                $scope.motion = Motion.get($scope.poll.motion_id);
                $scope.votesPrecision = MotionPollDecimalPlaces.getPlaces($scope.poll);
            }
            else {
                $scope.votesPrecision = 0;
            }
        });

        $scope.$watch(function () {
            return VotingController.lastModified(1) +
                AuthorizedVoters.lastModified(1) +
                Config.lastModified();
        }, function () {
            // Using timeout seems to give the browser more time to update the DOM.
            draw = true;
            $timeout(drawDelegateBoard, 0);
        });

        var drawDelegateBoard = function () {
            if (!draw) {
                return;
            }
            if (!Config.get('voting_show_delegate_board').value || !$scope.poll ||
                !$scope.motion) {
                // Only show the delegate board if the poll is published.
                $scope.delegateBoardHtml = '';
                draw = false;
                return;
            }

            // Get authorized voters.
            var av = AuthorizedVoters.get(1);
            var voters = av.authorized_voters;
            var showKey = av.type.indexOf('votecollector') === 0 && Config.get('voting_show_number').value;
            if (_.keys(voters).length > 0 &&
                av.type !== 'votecollector_anonymous' && av.type !== 'votecollector_secret') {
                // Create delegate board table cells.
                // console.log("Draw delegate board. Votes: " + MotionPollBallot.filter({poll_id: pollId}).length);
                var colCount = Config.get('voting_delegate_board_columns').value,
                    anonymous = Config.get('voting_anonymous').value || av.type === 'votecollector_pseudo_secret',
                    cells = [];
                _.forEach(voters, function (delegates, voterId) {
                    _.forEach(delegates, function (id) {
                        var user = User.get(id),
                            mpb = MotionPollBallot.filter({poll_id: pollId, delegate_id: id}),
                            name = Delegate.getCellName(user),
                            label = '',
                            number = 0,
                            cls = '';
                        if (showKey) {
                            number = Delegate.getKeypad(voterId).number;
                            label = number;
                        }
                        if (Config.get('voting_delegate_board_name').value !== 'no_name') {
                            label = number !== 0 ? number  + '<br/>' + name : name;
                        }
                        if (mpb.length === 1) {
                            // Set td class based on vote.
                            cls = anonymous ? 'seat-anonymous' : 'seat-' + mpb[0].vote;
                        }
                        cells.push({
                            name: name,
                            label: label,
                            number: number,
                            cls: cls,
                        });
                    });
                });

                // Build table. Cells are ordered by number or name.
                var table = '<table class="zoomcontent">',
                    sortKey = (Config.get('voting_sort_by_number').value && showKey) ? 'number' : 'name',
                    i = 0;
                _.forEach(_.sortBy(cells, sortKey), function (cell) {
                    if (i % colCount === 0) {
                        table += '<tr>';
                    }
                    table += '<td class="seat ' + cell.cls + '" ' +
                        'style="font-size: 1.0em;width: calc(100%/' + colCount + ');">' +
                        cell.label + '</td>';
                    i++;
                });

                $scope.delegateBoardHtml = table;
            }
            else {
                // Clear delegate table.
                $scope.delegateBoardHtml = '';
            }
            draw = false;
        };
    }
])

.controller('SlideAssignmentPollCtrl', [
    '$filter',
    '$scope',
    '$timeout',
    'AuthorizedVoters',
    'Config',
    'Assignment',
    'AssignmentPoll',
    'AssignmentPollBallot',
    'AssignmentPollDecimalPlaces',
    'User',
    'Delegate',
    'VotingController',
    function ($filter, $scope, $timeout, AuthorizedVoters, Config, Assignment, AssignmentPoll,
              AssignmentPollBallot, AssignmentPollDecimalPlaces, User, Delegate, VotingController) {
        // Each DS resource used here must be yielded on server side in ProjectElement.get_requirements!
        var pollId = $scope.element.id,
            draw = false; // prevents redundant drawing

        $scope.$watch(function () {
            // AssignmentPoll watch implies Assignment watch! So there is no need for an extra Assignment watcher.
            return AssignmentPoll.lastModified(pollId);
        }, function () {
            $scope.poll = AssignmentPoll.get(pollId);
            if ($scope.poll !== undefined) {
                $scope.assignment = Assignment.get($scope.poll.assignment_id);
                $scope.votesPrecision = AssignmentPollDecimalPlaces.getPlaces($scope.poll);
            }
            else {
                $scope.votesPrecision = 0;
            }
            draw = true;
            $timeout(drawDelegateBoard, 0);
        });

        $scope.$watch(function () {
            return AuthorizedVoters.lastModified(1);
        }, function () {
            // Get poll type for assignment.
            $scope.av = AuthorizedVoters.get(1);

            // Using timeout seems to give the browser more time to update the DOM.
            draw = true;
            $timeout(drawDelegateBoard, 0);
        });

        $scope.$watch(function () {
            return VotingController.lastModified(1) +
                Config.lastModified();
        }, function () {
            // Using timeout seems to give the browser more time to update the DOM.
            draw = true;
            $timeout(drawDelegateBoard, 0);
        });

        var drawDelegateBoard = function () {
            if (!draw || !$scope.av) {
                return;
            }
            if (!Config.get('voting_show_delegate_board').value || !$scope.poll ||
                !$scope.assignment) {
                // Only show the delegate board if the poll is published.
                $scope.delegateBoardHtml = '';
                draw = false;
                return;
            }

            // Get authorized voters.
            var voters = $scope.av.authorized_voters;
            var showKey = $scope.av.type.indexOf('votecollector') === 0 && Config.get('voting_show_number').value;
            if (_.keys(voters).length > 0 &&
                $scope.av.type !== 'votecollector_anonymous' && $scope.av.type !== 'votecollector_secret') {
                // Create delegate board table cells.
                // console.log("Draw delegate board. Votes: " + AssignmentPollBallot.filter({poll_id: pollId}).length);
                var colCount = Config.get('voting_delegate_board_columns').value,
                    anonymous = Config.get('voting_anonymous').value || $scope.av.type === 'votecollector_pseudo_secret',
                    cells = [];
                var options = $filter('orderBy')($scope.poll.options, 'weight');

                _.forEach(voters, function (delegates, voterId) {
                    _.forEach(delegates, function (id) {
                        var user = User.get(id),
                            apb = AssignmentPollBallot.filter({poll_id: pollId, delegate_id: id}),
                            name = Delegate.getCellName(user),
                            label = '',
                            number = 0,
                            key = '',
                            cls = '';
                        if (showKey) {
                            number = Delegate.getKeypad(voterId).number;
                            label = number;
                        }
                        if (Config.get('voting_delegate_board_name').value !== 'no_name') {
                            label = number !== 0 ? number  + '<br/>' + name : name;
                        }
                        if (apb.length > 0) {
                            apb = apb[0];
                            // Set td class based on vote.
                            if (anonymous) {
                                cls = 'seat-anonymous';
                            } else if ($scope.poll.pollmethod === 'votes') {
                                switch (apb.vote) {
                                    // global no and abstain
                                    case 'N':
                                        cls = 'seat-N'; break;
                                    case 'A':
                                        cls = 'seat-A'; break;
                                    case 'invalid':
                                        cls = 'seat-invalid'; break;
                                    default:
                                        key = _.findIndex(options, function(o) { return o.candidate_id == apb.vote; }) + 1;
                                        cls = 'seat-voted'; break;
                                }
                            } else { // YNA and YN
                                if ($scope.poll.options.length === 1) {
                                    cls = 'seat-' + apb.vote[$scope.poll.options[0].candidate_id];
                                } else {
                                    cls = 'seat-voted';
                                }
                            }
                        }
                        cells.push({
                            name: name,
                            label: label,
                            number: number,
                            cls: cls,
                            key: key,
                        });
                    });
                });

                // Build table. Cells are ordered by number or name.
                var table = '<table>',
                    sortKey = (Config.get('voting_sort_by_number').value && showKey) ? 'number' : 'name',
                    i = 0;
                _.forEach(_.sortBy(cells, sortKey), function (cell) {
                    if (i % colCount === 0) {
                        table += '<tr>';
                    }
                    table += '<td class="seat ' + cell.cls + '" ' +
                        'style="font-size: 1.0em;width: calc(100%/' + colCount + ');">';
                    if (cell.key) {
                        table +='<span class="key">' + cell.key + '</span>'
                    }
                    table += cell.label + '</td>';
                    i++;
                });

                $scope.delegateBoardHtml = table;
            }
            else {
                // Clear delegate table.
                $scope.delegateBoardHtml = '';
            }
            draw = false;
        };
    }
]);

}());
