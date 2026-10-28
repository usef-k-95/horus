/* Horus Intake helper.
 *
 * macOS lets a background job (launchd) read the Desktop, Documents and Downloads folders only after the
 * user has allowed it, and it remembers that permission per application. A plain /bin/sh started by
 * launchd cannot be allowed in a sensible way, so the watcher is started through this tiny application
 * instead: macOS asks once, "Horus Intake would like to access files in your Desktop folder", and the
 * answer covers everything this process starts (the shell loop, the Python tools, the unattended Horus
 * runs), because it stays alive as their responsible process.
 *
 * Usage: horus-intake PROGRAM [ARGS...]   runs PROGRAM, forwards termination signals, returns its exit code.
 * Built and signed by tools/intake.sh into ~/Horus/Horus Intake.app; it has no interface and no Dock icon.
 */
#include <errno.h>
#include <signal.h>
#include <spawn.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <unistd.h>

extern char **environ;
static pid_t child = 0;

static void forward(int sig) {
    if (child > 0) kill(-child, sig); /* the whole process group: the shell loop and its sleep */
}

int main(int argc, char **argv) {
    if (argc < 2) {
        fprintf(stderr, "usage: horus-intake PROGRAM [ARGS...]\n");
        return 2;
    }
    posix_spawnattr_t attr;
    posix_spawnattr_init(&attr);
    posix_spawnattr_setflags(&attr, POSIX_SPAWN_SETPGROUP);
    posix_spawnattr_setpgroup(&attr, 0);
    signal(SIGTERM, forward);
    signal(SIGINT, forward);
    signal(SIGHUP, forward);
    int rc = posix_spawn(&child, argv[1], NULL, &attr, argv + 1, environ);
    posix_spawnattr_destroy(&attr);
    if (rc != 0) {
        fprintf(stderr, "horus-intake: cannot start %s: %s\n", argv[1], strerror(rc));
        return 127;
    }
    int status = 0;
    while (waitpid(child, &status, 0) < 0) {
        if (errno != EINTR) {
            perror("horus-intake: waitpid");
            return 1;
        }
    }
    if (WIFEXITED(status)) return WEXITSTATUS(status);
    if (WIFSIGNALED(status)) return 128 + WTERMSIG(status);
    return 1;
}
