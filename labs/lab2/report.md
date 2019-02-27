# Lab 2 Report

## Common Setuid Linux Programs

All three of the following programs have the `setuid` bit set.

* `/usr/bin/passwd`

  ![`passwd` is a `setuid` program](figures/1-password.png)

* `/bin/su`

  ![`su` is a `setuid` program](figures/1-su.png)

* `/usr/bin/sudo`

  ![`sudo` is a `setuid` program](figures/1-sudo.png)

This means that if an ordinary user runs these programs, they will temporarily have elevated root
privileges while they run the program. This makes sense given that each of these programs require
higher permissions than many of their counterparts because they deal with user authentication and
related tasks.

So what happens if they are no longer `setuid` programs owned by the root user?

First, I copied each of the programs to a temporary directory owned by the `seed` user. This act
always unsets the `setuid` bit. Then, I attempted to run each of the three programs to observe their
behavior. I attempted to change the password for the `seed` user. The normal behavior of the `passwd(1)`
command is for a normal user to run the program (without `sudo`) and update their own password,
provided that they are able to successfully input their own password.

What happened when I ran the program without the `setuid` bit set is that it failed to set the `seed`
user's password. This is expected, because the password files are owned by root, so `passwd` must
somehow obtain root privileges. This is accomplished through the `setuid` bit, and the fact that
`passwd` is owned by root. Thus whenever a user runs the program, they are able to update the
system password files.

![`passwd` behavior without the `setuid` bit set](figures/1-run-passwd.png)

A similar failure occurred when I attempted to login to the `root` account from the `setuid`-less
`su` command. Since `su` did not have the `setuid` bit set, it was unable to obtain the elevated
privileges necessary to switch user accounts, even though the correct password was entered.

![`su` behavior without the `setuid` bit set](figures/1-run-su.png)

Similarly, when I attempted to change the ownership of a `root`-owned file with the `setuid`-less
`sudo` program, it failed for the same reason. However, note that this time it failed with a more
descriptive error message indicating that the `sudo` executable must have the `setuid` bit set *and*
be owned by `root`.

As an aside, I think it's interesting that the `sudo` program checks its own permissions and owner.

![`sudo` behavior without the `setuid` bit set](figures/1-run-sudo.png)

## Differences in Bash and Zsh

Here, I copied `/bin/bash` and `/bin/zsh` to `/tmp/` and ensured they were owned by `root` and had
the `setuid` bit set. Then after running each of the two shells, I executed the `whoami` command in
each shell.

![A summary of the `setuid` differences between Bash and Zsh](figures/2-setuid-summary.png)

When I ran `whoami` in the `zsh` shell session, it indicated that I was running the shell as the
`root` user. This is surprising, because I ran the `zsh` shell session *as the `seed` user*. So since
the `setuid` bit was set on the `zsh` executable, and the executable was owned by `root`, anyone
executing it will obtain `root` privileges for the duration of the shell session.

On the contrary, when I ran `whoami` in the `bash` shell session, it indicated that I was running the
shell as the `seed` user. This is also surprising given the results above with the `zsh` shell.

The difference is that Bash looks at the actual user id rather than the effective user id when checking
permissions. Each shell has the available permissions, being a `setuid` program owned by `root`, to
give the shell session access to the root user. However, Bash made a decision to use the actual user id
when setting the session user, so even though it is able to log in as the `root` user, it chooses
not to, likely as a security consideration.

## Setting the System `/bin/sh`

By default, Ubuntu systems symlink `/bin/sh` to `/bin/dash` (*not* `/bin/bash`!) in order to use `dash(1)`
as the default shell.

![`/bin/sh` is a symlink to `/bin/dash`](figures/3-sh-ln-dash.png)

`dash(1)` is a much more limited shell that aims to be POSIX compliant while being as small as possible.
Thus, while it is the default shell used to execute scripts, we almost always add the shebang `#!/bin/bash`
to the top of shell scripts in order to execute them with a more powerful shell, `bash(1)`.

However, for the rest of the lab, I symlinked `/bin/sh` to `/bin/zsh`.

![Changing `/bin/sh` to link to `/bin/zsh`](figures/3-sh-ln-zsh.png)

## Running Unintended Programs via the `PATH` Environment Variable

Then I wrote and compiled the following extremely complicated C program that runs the `ls` command using `system(3)`.

```c
int main()
{
    system("ls");
    return 0;
}
```

Note that the man page for `system(3)` contains the following paragraph on the dangers of `setuid`.

![A portion of the `system(3)` man page](figures/system-manpage.png)

The reason this is a security vulnerability, is that `system(3)` uses `/bin/sh` to run the given command
in a new shell created with a copy of the current environment. Thus if you add a malicious program
to the beginning of your executable search `PATH`, you can run an arbitrary program with whatever
privileges the intended program was able to run with. This is because the search `PATH` is searched
from beginning to end for the desired program, and `/bin/sh` will run the first match found.

So if we inject our own version of `ls` at the beginning of our `PATH`, we can trick `/bin/sh` into
running our own program in place of the intended `/bin/ls`, *and do so with root privileges.*

To demonstrate this, I copied `/usr/bin/whoami` to my `lab2` directory and renamed it `ls`.

![Copying `/usr/bin/whoami` to my `lab2/` directory](figures/4-ls-whoami.png)

Then I compiled the above program, and changed the resultant executable to a `root`-owned `setuid`
program, and ran it before and after adding `~/Desktop/lab2` to my `PATH` environment variable.

![Running my own version of `ls` with escalated privileges](figures/4-a-use-own-ls-with-root.png)

Notice that not only was I able to convince `/bin/sh` to run my own malicious version of `ls`, I was
able to do so *with `root` privileges!* Thus the `system(3)` man page is correct, *do not use `system(3)`*
*from a `setuid` program!*

Now we symlinked `/bin/sh` to `/bin/zsh` above, but earlier we saw a difference in how `bash` treated
setuid programs opposed to `zsh`. So I symlinked `/bin/sh` to `bash` and to `dash` in order to compare
the results. What I saw was surprising.

![Running my own version of `ls` using Bash](figures/4-bash.png)

![Running my own version of `ls` using Dash](figures/4-dash.png)

All three of Zsh, Bash, and Dash ran the malicious imposter `ls` as root. From above, and from the
language in the lab assignment, I expected Bash to avoid doing so. However, this is not the behavior
I observed.

I think that the difference is that before, Bash itself was a `setuid` program running `whoami`. Here,
Bash is being ran *from a `setuid` program*, and is unable to perform the necessary introspection to
limit the user privileges.

## The Difference Between `system(3)` and `execve(2)`

So if using `system(3)` from a `setuid` program is off the table, what is the appropriate method for
running system commands? This portion of the lab examines one of the important differences between
`system(3)` and its related counterpart `execve(2)`.

I wrote and compiled the following program

```c
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

int main( int argc, char** argv )
{
    char* v[3];
    if( argc < 2 )
    {
        printf( "Please enter a filename.\n" );
        return 1;
    }

    v[0] = "/bin/cat";
    v[1] = argv[1];
    printf( "filename: %s\n", argv[1] );
    v[2] = 0;

    // Set q = 0 or 1 for questions a and b rexpectively.
    int q = 0;

    if( q == 0 )
    {
        char* command = malloc( strlen(v[0]) + strlen(v[1]) + 2 );
        sprintf( command, "%s %s", v[0], v[1] );
        system( command );
    }
    else
    {
        execve( v[0], v, 0 );
    }

    return 0;
}
```

Notice that this is slightly different than the code listed in the lab assignment. I chose to print
the "filename" being passed through `argv[1]` to `/bin/cat`. This helped debug the program behavior
and enabled a deeper understanding of the `system(3)` behavior.

This program takes in a single commandline argument and passes that argument as a "filename" to `/bin/cat`.
So my goal was to trick `system(3)` into running arbitrary code with elevated root privileges. Recalling
from wherever I learned it, *Your shell* is responsible for parsing commandline arguments and passing those
to your program, including glob (`*`) expansion, special variable expansion (`~`), and normal variable
expansion (`$PATH`). One of the semantics of most shells, including those on Windows, is to treat arguments
surrounded with quotes *as a single argument* rather than splitting on spaces into multiple arguments.

This is why I added the extra `printf` in the program to display the argument, because it helped me
convince myself of exactly what is going on. Thus, I ran the program with the argument

```text
`/root/file && touch /root/test`
```

so that `system` would execute the entire command rather than splitting on spaces, or on logical
operators and execute only the first `/bin/cat` command as `root`. Other tricks using the special
Bash operators `|`, `>`, etc work identically.

![Using `system(3)` with commandline arguments](figures/5-a.png)

The result is as expected; with the quotes, Bash parsed the entire command as the first commandline
argument, so that `system` executed the entire thing with elevated permissions. Without the quotes,
Bash parsed the command as multiple commandline arguments; first the command `./ccat /root/file`, performed
with elevated privileges, and second the command `touch /root/test` *without* elevated privileges.

This is a gaping security vulnerability, and one that can easily be fixed by replacing `system(3)` in
the `setuid` program with `execve(2)`. The difference between the two functions is that `system(3)`
runs an arbitrary shell command using `/bin/sh`, while `execve(2)` runs *a single executable program*
with an array of commandline arguments. Thus, it is not possible to trick `execve(2)` into executing
arbitrary shell commands as opposed to `system(3)`.

![Using `execve(2)` with commandline arguments](figures/5-b.png)

Here, using `execve`, the quoted commandline argument is treated as a single argument, rather than
being parsed by `/bin/sh` and then being ran.

## Overriding Runtim Dynamic Libraries With `LD_PRELOAD`

We can use the powerful `LD_PRELOAD` environment variable to force the runtime dynamic linker to use
our own custom (and possibly malicious) version of a dynamically linked library function in place of
the intended one. This variable is extremely useful in ordinary development practices, but is also
commonly leveraged in system exploitation.

Now, in the context of `setuid` programs, the runtime linker treats programs differently in some
conditions.

First, I created a dynamic library containing a function implementing the

```c
void sleep( int );
```

interface. Since the purpose of this lab is merely an educational proof of concept rather than an
actual attempt to perform anything malicious, I wrote the function

```c
#include <stdio.h>

void sleep( int s )
{
    printf( "I am not sleeping %d secs!\n", s );
}
```

and compiled it into a dynamic library with the commands

```shell
gcc -fPIC -g -c mylib.c
gcc -shared -Wl,-soname,libmylib.so.1 -o libmylib.so.1.0.1 mylib.o -lc
```

![Compiling the dynamic library](figures/6-a-b.png)

Then in order to test the library, I wrote the small program

```c
int main()
{
    sleep( 1 );
    return 0;
}
```

Then I set the `LD_PRELOAD` environment variable with the command

```shell
export LD_PRELOAD=./libmylib.so.1.0.1
```

and ran the program with different permissions and users to observe the results. If our `LD_PRELOAD`
injection was successful, the program will print `I am not sleeping 1 secs!` to the console and then
exit. If our injection failed, the program will link against the libc implementation of `void sleep( int )`,
which actually sleeps for the given number of seconds.

First, I ran the program with the usual permissions and user. This resulted in a successful `LD_PRELOAD` injection.

![Running the program as a normal user](figures/6-d-a-seed-seed.png)

Then I made the `myprog` program a `setuid` program owned by root, and ran it as a normal user. This
did not result in the `LD_PRELOAD` injection working.

![Running the `setuid` root program as a normal user](figures/6-d-b-root-seed.png)

But then when I ran the program again as the root user, it *did* result in a successful injection.

![Running the `setuid` root program as root](figures/6-d-c-root-root.png)

Finally, I created a new `user1` user and changed `myprog` to be owned by `user1` and to be a
`setuid` program. Running this program as the `seed` user did not result in a successful injection
attack.

![Running the `setuid` `user1` program as `seed`](figures/6-d-d-user1-seed.png)

But running the program again as the `user1` user confirmed my suspicion that the runtime linker
only makes use of the `LD_PRELOAD` environment variable on `setuid` programs if the user running the
program is its owner.

![Running the `setuid` program as `user1`](figures/6-d-e-user1-user1.png)

The following snippet from the `ld.so(8)` man page confirms this suspicion.

> Secure-execution mode
>
> For security reasons, the effects of some environment variables
> are voided or modified if the dynamic linker determines that the
> binary should be run in secure-execution mode. (For details, see
> the discussion of individual environment variables below.)  A
> binary is executed in secure-execution mode if the `AT_SECURE` entry
> in the auxiliary vector (see `getauxval(3)`) has a nonzero value.
> This entry may have a nonzero value for various reasons, including:
>
> * The process's real and effective user IDs differ, or the real
>   and effective group IDs differ. This typically occurs as a
>   result of executing a set-user-ID or set-group-ID program.
>
> * A process with a non-root user ID executed a binary that
>   conferred capabilities to the process.
>
> * A nonzero value may have been set by a Linux Security Module.

Later in the man page, it states the following specifically about the `LD_PRELOAD` environment
variable.

> In secure-execution mode, preload pathnames containing slashes
> are ignored. Furthermore, shared objects are preloaded only
> from the standard search directories and only if they have
> set-user-ID mode bit enabled (which is not typical).

So there are two reasons `ld.so` refused to link our imposter `void sleep( int )` function. First,
our pathname in `LD_PRELOAD` contained a slash, and was thus ignored. Second, share objects are
preloaded only from the standard search directories if the `setuid` bit is set.

The reason we were able to successfully inject our imposter function when running the non-`setuid`
program as the `seed` user was that secure-execution mode was never triggers. Secure-execution mode
was also not triggered when running the `user1` `setuid` program as the `user1` user, and the `root`
`setuid` program as the `root` user because the real and effective user IDs did not differ in those
cases.

This also explains why the injection failed when running the program with `sudo`, but succeeded in
the `sudo bash` environment. When running the program with `sudo`, the real and effective user IDs
are not the same. But when running `sudo bash`, you become the `root` user, instead of temporarily
assuming root privileges. Thus in the second case, the real and effective user IDs are the same.

## Relinquishing Setuid Privileges and `open(2)`

In this portion of the lab, I examined how programs should properly relinquish root privileges once
they are finished with them. This is a good practice, because it diminishes the available attack
surface to take advantage of.

One of the methods to relinquish root privileges is to use the `setuid(2)` and `getuid(2)` functions
to set the user ID to the real user ID (`geteuid(2)` gets the effective user ID).

To examine one of the considerations of relinquishing escalated privileges, I wrote and ran the
following program.

```c
#include<fcntl.h>
#include<stdio.h>
#include<stdlib.h>
#include<sys/stat.h>
#include<sys/types.h>

int main()
{
    // Assume that /etc/zzz is an important system file owned by root with
    // permission 0644.
    int fd = open( "/etc/zzz", O_RDWR | O_APPEND );
    if( fd < 0 )
    {
        printf( "Cannot open '/etc/zzz'\n" );
        return 1;
    }

    // ...

    // Now relenquish the root privileges.
    // Note that getuid() returns the real uid.
    setuid( getuid() );

    if( fork() )
    {
        close( fd );
        return 0;
    }
    else
    {
        // Now assume attackers have injected malicious code, possibly
        // with LD_PRELOAD here.
        write( fd, "Malicious Data\n", 15 );
        close( fd );
    }

    return 0;
}
```

Note that because the program `fork(2)`'s the process after relinquishing its root privileges,
`ld.so(8)` will not enter the secure-execution mode discussed above, so it should be possible to
use `LD_PRELOAD` to inject arbitrary code in any dynamically loaded function calls in the child
process.

What I noticed from this program, is that I was still able to write to a `root`-owned file
*even after the escalated privileges were relinquished!*

![The program writing malicious data even after root privileges were relinquished](figures/7-open-root-fd.png)

My suspicion was that this was a consequence of using `fork(2)`, but that turned out to not be the
case. The following similar program also exhibited the same behavior.

```c
#include<fcntl.h>
#include<stdio.h>
#include<stdlib.h>
#include<sys/stat.h>
#include<sys/types.h>

int main()
{
    int fd = open( "/etc/zzz", O_RDWR | O_APPEND );
    if( fd < 0 )
    {
        printf( "Cannot open '/etc/zzz'\n" );
        return 1;
    }

    setuid( getuid() );

    write( fd, "Malicious Data\n", 15 );
    close( fd );

    return 0;
}
```

This is because file permissions are checked when the file is *opened*, and not on subsequent writes.
If we modify the program to attempt to open the root file again after relinquishing the root
privileges it will fail to write the second line of malicious data.

Further, the `fork(2)` man page states the following

> The child inherits copies of the parent's set of open file descriptors.
> Each file descriptor in the child refers to the same open file description
> (see `open(2)`) as the corresponding file descriptor in the parent. This means
> that the two file descriptors share open file status flags, file offset, and
> signal-driven I/O attributes (see the description of `F_SETOWN` and `F_SETSIG`
> in `fcntl(2)`).

This means that the child process will be able to read and/or write to any open files from the parent
process, depending on the mode they were opened in. Thus any files opened with root privileges
should be closed before any privileges are relinquished, and definitely before the program is forked.

```c
#include<fcntl.h>
#include<stdio.h>
#include<stdlib.h>
#include<sys/stat.h>
#include<sys/types.h>

int main()
{
    int fd = open( "/etc/zzz", O_RDWR | O_APPEND );
    if( fd < 0 )
    {
        printf( "Cannot open '/etc/zzz'\n" );
        return 1;
    }

    setuid( getuid() );

    // This write will succeed.
    write( fd, "Malicious Data\n", 15 );
    close( fd );

    fd = open( "/etc/zzz", O_RDWR | O_APPEND );
    // We cannot open the file without the root privileges
    if( fd < 0 )
    {
        printf( "Cannot open '/etc/zzz'\n" );
        return 1;
    }

    // This write will fail.
    write( fd, "Malicious Data\n", 15 );
    close( fd );

    return 0;
}
```

Now, as the above discussion of `LD_PRELOAD` indicates, it may be difficult to inject malicious code
to write the malicious data without forking, because `ld.so(8)` will ignore `LD_PRELOAD` if the real
and effective user IDs running the program differ.

But if the program is forked, the real and effective user IDs of the child process will match, and I
believe that an `LD_PRELOAD` injection will be successful. Due to time constraints, I did not test
this theory.
