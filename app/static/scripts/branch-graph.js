document.addEventListener('DOMContentLoaded', () => {
    const branches = document.querySelectorAll('.branch');
    const connectionsContainer = document.getElementById('connections');
    const branchColors = {};
    const allCommits = [];

    // Generate unique colors for each branch
    function getRandomColor() {
        return `hsl(${Math.random() * 360}, 70%, 50%)`; // Vibrant random color
    }

    // Assign colors and collect commits with timestamps
    branches.forEach(branch => {
        const branchName = branch.dataset.branch;

        // Assign a color if not already assigned
        if (!branchColors[branchName]) {
            branchColors[branchName] = getRandomColor();
        }

        // Apply the branch color
        branch.style.setProperty('--branch-color', branchColors[branchName]);

        // Update branch label color
        const label = branch.querySelector('.branch-label');
        if (label) {
            label.style.backgroundColor = branchColors[branchName];
        }

        // Collect commits for chronological sorting
        const commits = branch.querySelectorAll('.commit');
        commits.forEach(commit => {
            allCommits.push({
                element: commit,
                date: new Date(commit.dataset.date), // Assuming data-date contains the ISO timestamp
            });
        });
    });

    // Sort all commits by date
    allCommits.sort((a, b) => a.date - b.date);

    // Position commits based on chronological order
    allCommits.forEach((commit, index) => {
        const position = (index / (allCommits.length - 1)) * 100;
        commit.element.style.left = `${position}%`;
    });

    // Function to create connections
    function createConnection(nodeA, nodeB) {
        const rectA = nodeA.getBoundingClientRect();
        const rectB = nodeB.getBoundingClientRect();

        // Calculate start and end points
        const x1 = rectA.left + rectA.width / 2;
        const y1 = rectA.top + rectA.height / 2;
        const x2 = rectB.left + rectB.width / 2;
        const y2 = rectB.top + rectB.height / 2;

        // Calculate distance and angle
        const length = Math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2);
        const angle = Math.atan2(y2 - y1, x2 - x1) * (180 / Math.PI);

        // Create line element
        const line = document.createElement('div');
        line.className = 'connection';
        line.style.width = `${length}px`;
        line.style.transform = `rotate(${angle}deg)`;
        line.style.left = `${x1}px`;
        line.style.top = `${y1}px`;

        connectionsContainer.appendChild(line);
    }

    // Create connections between shared commits
    const sharedCommits = {{ repo.shared_commits | safe
}};
for (const [sha, branches] of Object.entries(sharedCommits)) {
    if (branches.length > 1) {
        for (let i = 0; i < branches.length - 1; i++) {
            const nodeA = document.querySelector(
                `.commit[data-branch="${branches[i]}"][data-sha="${sha}"]`
            );
            const nodeB = document.querySelector(
                `.commit[data-branch="${branches[i + 1]}"][data-sha="${sha}"]`
            );

            if (nodeA && nodeB) {
                createConnection(nodeA, nodeB);
            }
        }
    }
}
});
