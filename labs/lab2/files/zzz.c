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
