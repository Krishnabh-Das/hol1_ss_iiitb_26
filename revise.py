from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm

out="D:/IIITB/Mtech_1st_year/SS/Hands_on_list_1Hands-on List 1.pdf"

styles=getSampleStyleSheet()
title=ParagraphStyle("Title2", parent=styles["Title"], fontSize=22, leading=27, alignment=TA_CENTER, spaceAfter=10)
sub=ParagraphStyle("Sub", parent=styles["Normal"], fontSize=10.5, leading=15, alignment=TA_CENTER, textColor=colors.grey)
h1=ParagraphStyle("H1", parent=styles["Heading1"], fontSize=16, leading=20, spaceBefore=8, spaceAfter=8)
h2=ParagraphStyle("H2", parent=styles["Heading2"], fontSize=12, leading=15, spaceBefore=6, spaceAfter=5)
body=ParagraphStyle("Body", parent=styles["BodyText"], fontSize=9.2, leading=13, spaceAfter=5)
small=ParagraphStyle("Small", parent=styles["BodyText"], fontSize=8.2, leading=11, spaceAfter=3)
code=ParagraphStyle("Code", parent=styles["Code"], fontName="Courier", fontSize=7.3, leading=9.3, leftIndent=8, rightIndent=8, spaceBefore=3, spaceAfter=5)
qa=ParagraphStyle("QA", parent=body, leftIndent=7)
difficulty=ParagraphStyle("Diff", parent=styles["BodyText"], fontSize=9, leading=12, alignment=TA_CENTER)

def P(x, style=body):
    return Paragraph(x.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;"), style)

def codeblock(x):
    return Paragraph(x.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace("\n","<br/>"), code)

def Q(q,a):
    return [P("<b>Q:</b> "+q, qa), P("<b>A:</b> "+a, qa)]

doc=SimpleDocTemplate(out,pagesize=A4,rightMargin=15*mm,leftMargin=15*mm,topMargin=14*mm,bottomMargin=14*mm)
story=[]
story += [P("SYSTEM SOFTWARE — VIVA MASTER GUIDE",title),
          P("30 Lab Questions • Code flow • OS/Linux concepts • Follow-up viva questions",sub),
          Spacer(1,8),
          P("<b>How to use this tonight:</b> For every random question, be able to explain (1) what the program is trying to do, (2) the execution flow, (3) what each important system/library call does, (4) what happens inside the OS at a high level, and (5) the likely “what if?” questions.",body),
          P("<b>Source basis:</b> The uploaded lab sheet contains 30 exercises covering file/process management and process management. fileciteturn0file0L2-L8",small)]
# citation markup won't render correctly; replace with plain source note
story[-1]=P("<b>Source basis:</b> The uploaded lab sheet lists 30 exercises covering file/process management and process management.",small)

diffs=[
("Q1","Medium"),("Q2","Easy"),("Q3","Easy"),("Q4","Medium"),("Q5","Medium"),("Q6","Medium"),
("Q7","Medium"),("Q8","Medium"),("Q9","Medium"),("Q10","Medium"),("Q11","Hard"),("Q12","Medium"),
("Q13","Hard"),("Q14","Medium"),("Q15","Medium"),("Q16","Hard"),("Q17","Hard"),("Q18","Hard"),
("Q19","Hard"),("Q20","Medium"),("Q21","Easy"),("Q22","Hard"),("Q23","Medium"),("Q24","Easy"),
("Q25","Medium"),("Q26","Medium"),("Q27","Hard"),("Q28","Medium"),("Q29","Hard"),("Q30","Hard")]

questions=[
("1. Links and FIFO","Medium","Create soft link, hard link and FIFO using shell commands and system calls.",
"""<b>Core:</b> A soft link is a separate filesystem object that refers to a pathname. A hard link is another directory entry for the <i>same inode</i>. A FIFO is a named pipe used for IPC.<br/><br/>
<b>Commands:</b> <font name='Courier'>ln -s original soft</font> • <font name='Courier'>ln original hard</font> • <font name='Courier'>mkfifo myfifo</font>.<br/>
<b>Calls:</b> <font name='Courier'>symlink(target, linkname)</font> • <font name='Courier'>link(old,new)</font> • <font name='Courier'>mkfifo(path,mode)</font>. <font name='Courier'>mknod</font> can also create special files at a lower level.<br/>
<b>Flow:</b> syscall/library interface → kernel → filesystem object/directory entry → return success or -1 with errno. 0666 is filtered by umask.""",
[("Why can a symlink point to a missing file?","It stores a pathname/reference; target resolution happens later. Such a link is dangling."),
("Why can a hard link survive deletion of the original name?","Both names point to the same inode. Data remains while at least one directory entry/reference keeps the inode alive."),
("What is a FIFO?","A named pipe: a kernel-managed IPC endpoint represented in the filesystem; readers and writers communicate through it."),
("What is the big difference?","Soft link → path/reference and separate inode. Hard link → same inode. FIFO → IPC object, not ordinary persistent file contents.")]),
("2. Background infinite loop and /proc","Easy","Run an infinite-loop process in the background and inspect its /proc directory.",
"""<b>Flow:</b> <font name='Courier'>fork is not required here</font>; run the program with <font name='Courier'>&amp;</font>. The program calls <font name='Courier'>getpid()</font>, prints its PID, then repeatedly sleeps. <font name='Courier'>sleep(1)</font> prevents a busy loop.<br/>
<b>/proc:</b> a virtual filesystem populated by the kernel. <font name='Courier'>/proc/PID/status</font> shows process state/PID/PPID and other information; <font name='Courier'>fd/</font> shows open descriptors; <font name='Courier'>exe</font>, <font name='Courier'>cwd</font>, <font name='Courier'>maps</font>, <font name='Courier'>stat</font> and others expose process information.""",
[("Why does /proc/PID disappear after the process exits?","It represents live kernel process information; once the process is gone, its proc entry is gone."),
("Why sleep?","To keep the process alive while avoiding unnecessary CPU consumption."),
("What does State=S usually mean here?","Sleeping; the process is waiting in sleep rather than executing.")]),
("3. creat() and file descriptor","Easy","Create a file and print its file descriptor.",
"""<b>Core:</b> <font name='Courier'>creat(path,mode)</font> creates a file or opens an existing one for writing and truncates it. It returns a small integer FD, or -1 on error.<br/>
<b>FD basics:</b> 0=stdin, 1=stdout, 2=stderr. If all are occupied, the next commonly available FD is 3, but the rule is actually the <i>lowest available</i> descriptor.""",
[("What does creat do if the file exists?","It truncates it to zero length and opens it for writing."),
("What does 0644 mean?","Owner read/write; group read; others read, subject to umask."),
("What is an FD?","A per-process integer handle referring to an open kernel object/open file description.")]),
("4. open O_RDWR and O_EXCL","Medium","Open an existing file read/write and try exclusive creation.",
"""<b>O_RDWR:</b> read + write; does not create a missing file.<br/>
<b>O_CREAT:</b> create if absent. <b>O_EXCL + O_CREAT:</b> fail if the pathname already exists, typically with EEXIST. The mode argument matters when a new file is created.<br/>
<b>Important:</b> access mode (O_RDONLY/O_WRONLY/O_RDWR) is different from filesystem permission bits such as 0644.""",
[("What if existing.txt is missing in the first open?","O_RDWR alone fails; it does not create."),
("What does O_EXCL really guarantee?","With O_CREAT, it requests exclusive creation so an existing pathname causes failure; it is not a read/write permission flag."),
("Why can O_EXCL be useful?","It prevents two creators from both believing they exclusively created the same pathname.")]),
("5. Five files and /proc/PID/fd","Medium","Create five files, keep the process alive, and inspect its FD table.",
"""Open five files with O_CREAT|O_RDWR. Store the returned descriptors in an array. If 0/1/2 are occupied, they will commonly be 3–7, but descriptors are always allocated from the lowest available numbers, so this is not guaranteed.<br/>
<b>/proc/PID/fd</b> contains symbolic links showing what each open descriptor refers to. The infinite loop keeps the process and descriptors alive for inspection.""",
[("Why store the FDs in an array?","So each descriptor can be retained and associated with its file."),
("What happens when the process exits?","Its descriptors are closed by the kernel and the /proc/PID entry disappears."),
("What does fd/ show?","Per-process descriptor entries, often as links to files, pipes, sockets, /dev objects, etc.")]),
("6. read STDIN and write STDOUT","Medium","Copy bytes from stdin to stdout using only read/write.",
"""<b>FDs:</b> STDIN_FILENO=0, STDOUT_FILENO=1. <font name='Courier'>read(fd,buf,n)</font> returns bytes read: &gt;0 data, 0 EOF, -1 error. <font name='Courier'>write</font> can return fewer bytes than requested, so robust code loops until the whole chunk is written.<br/>
<b>Important:</b> read/write are byte-oriented, not line-oriented. A buffer of 1024 means “request up to 1024 bytes per call”, not a universal system limit.""",
[("Why ssize_t?","It can represent a positive byte count, zero, and -1 for error."),
("Why might write be partial?","The destination may accept only part of the requested data, especially pipes/sockets/other non-regular destinations."),
("stderr vs stdout?","stderr is FD 2 and is typically unbuffered; stdout is FD 1 and is commonly line-buffered on a terminal and fully buffered when redirected."),
("Why fprintf(stderr,...)?","It sends diagnostic/error text to stderr, so stdout can remain clean and can be redirected independently."),
("What does perror do?","It prints a supplied prefix plus a human-readable message based on the current errno.")]),
("7. Copy file1 to file2","Medium","Implement cp-like copying using open/read/write.",
"""Open source O_RDONLY. Open destination O_WRONLY|O_CREAT|O_TRUNC with a mode such as 0644. Repeatedly read chunks and write them, handling partial writes. Close both FDs.<br/>
<b>O_TRUNC</b> clears an existing destination. This simple program copies file contents; full GNU cp also handles many metadata and special-file cases.""",
[("Why O_TRUNC?","So an old longer destination is not left with stale bytes after the new shorter contents."),
("Why loop read/write?","Files can be larger than the buffer, and write can be partial."),
("Why argc/argv?","The source and destination are supplied as command-line arguments.")]),
("8. fdopen and line-by-line reading","Medium","Open a file read-only, read line by line, print each line, and close at EOF.",
"""Typical flow: <font name='Courier'>open → FD → fdopen → FILE* → fgets → fputs → fclose</font>.<br/>
<font name='Courier'>fdopen</font> associates an existing FD with a stdio stream; it does not perform another open. <font name='Courier'>fgets</font> reads at most size-1 characters, retains a newline if one was read, null-terminates the string, and returns NULL at EOF/error. <font name='Courier'>fputs</font> does not add a newline. <font name='Courier'>fclose</font> closes the stream and underlying FD.""",
[("Why fdopen instead of fopen?","The program already has an FD from open and wants to use stdio functions such as fgets."),
("What if a line is longer than the buffer?","fgets returns it in pieces; multiple calls may be needed for one logical line."),
("Should we close the FD after fclose?","No; successful fclose closes the underlying descriptor.")]),
("9. stat() metadata","Medium","Print inode, links, UID/GID, size, block size/count and timestamps.",
"""<b>stat(path,&s)</b> asks the kernel/filesystem for metadata and fills <font name='Courier'>struct stat</font>. It does not need to read the file's contents.<br/>
Key fields: st_ino inode number; st_nlink hard-link count; st_uid/st_gid owner/group; st_size logical size; st_blksize preferred I/O block size; st_blocks allocated blocks (Linux commonly in 512-byte units); st_atime last access; st_mtime content modification; st_ctime inode/status change time—not creation time.<br/>
<b>stat vs lstat:</b> stat follows the final symlink; lstat reports the symlink itself.""",
[("Where does the information come from?","The pathname is resolved by the kernel; filesystem metadata associated with the inode/filesystem object is used to fill struct stat and copied to user memory."),
("Does st_size equal allocated storage?","Not necessarily. Sparse files can have a large logical size but fewer allocated blocks."),
("Is st_ctime creation time?","No. On Linux it is the last change to inode/status metadata, not a birth/creation timestamp.")]),
("10. lseek and sparse file","Medium","Write 10 bytes, move the file offset forward 10 bytes, then write another 10 bytes.",
"""After writing 10 bytes, the offset is 10. <font name='Courier'>lseek(fd,10,SEEK_CUR)</font> moves it to 20 and returns the new offset. No data is written by lseek. The next 10-byte write starts at offset 20, leaving a logical hole from offsets 10–19.<br/>
A sparse file can have logical size 30 while not allocating physical blocks for every hole byte. <font name='Courier'>od</font> can show the logical zero-filled hole; tools such as <font name='Courier'>ls -l</font> vs <font name='Courier'>ls -ls</font> help distinguish logical size and allocated blocks.""",
[("Why check lseek against (off_t)-1?","That is the failure return value; offsets use off_t."),
("What does SEEK_SET/CUR/END mean?","Offset from beginning/current position/end."),
("What is a hole?","A range in the logical file with no actual written data; reading it returns zeros, while storage may be unallocated.")]),
("11. dup, dup2 and fcntl duplication","Hard","Duplicate a descriptor and write through both descriptors.",
"""<b>Critical distinction:</b> duplicated FDs are different integers in the process FD table, but they refer to the <i>same open file description</i>. The open file description stores the current offset and file status flags.<br/>
<font name='Courier'>dup(fd)</font> returns the lowest available FD. <font name='Courier'>dup2(fd,newfd)</font> makes newfd refer to the same open file description, closing/replacing newfd first if needed. <font name='Courier'>fcntl(fd,F_DUPFD,min)</font> returns the lowest available FD ≥ min.<br/>
If O_APPEND was used, each write is positioned at the end. Two descriptors created by dup share the underlying offset/state.""",
[("Do dup and dup2 create another open file description?","No. They create another FD referring to the same open file description."),
("What if the file is opened twice separately?","Usually there are separate open file descriptions, so their offsets are independent."),
("What happens if one duplicate is closed?","The other duplicate remains usable; the underlying open state persists until all relevant references are gone."),
("Why does this matter after fork?","Parent and child inherited descriptors can also refer to the same open file description and therefore share the offset.")]),
("12. Find opening mode using fcntl","Medium","Use fcntl to determine whether an FD is read-only, write-only, or read/write.",
"""<font name='Courier'>fcntl(fd,F_GETFL)</font> retrieves file status flags associated with the open file description. To extract access mode, use <font name='Courier'>flags & O_ACCMODE</font> and compare against O_RDONLY/O_WRONLY/O_RDWR.<br/>
Do not switch on the entire flags value because it can contain unrelated status flags such as O_APPEND. Access mode is also different from filesystem permissions like 0644.""",
[("Why O_ACCMODE?","It masks out unrelated status flags and leaves the access-mode bits."),
("If this exact program opened O_RDWR, what will it print?","Read/write; it is querying the mode it itself requested."),
("What is F_GETFL?","A fcntl command for retrieving file status flags.")]),
("13. select for 10 seconds","Hard","Wait for stdin readiness for up to 10 seconds.",
"""<font name='Courier'>select(nfds, readfds, writefds, exceptfds, timeout)</font> waits for I/O readiness. For stdin only, nfds is <font name='Courier'>STDIN_FILENO+1</font>, i.e. 1, because select considers descriptors 0 through nfds-1. It is <i>not</i> the number of descriptors.<br/>
FD_SET macros prepare fd_sets: FD_ZERO clears, FD_SET adds, FD_ISSET tests after select. readfds means a read can proceed without blocking (EOF also counts as readable). writefds means write readiness. exceptfds is for exceptional conditions. timeout is maximum wait: NULL=infinite, {10,0}=up to 10s, {0,0}=no wait.<br/>
Return: &gt;0 ready descriptors, 0 timeout, -1 error. select only reports readiness; read/write performs the actual I/O. It modifies the fd_sets, so repeated calls normally rebuild them.""",
[("Why nfds = STDIN_FILENO+1?","select expects one more than the highest FD being monitored."),
("Does select read the data?","No. It says that a read should not block; the program still calls read()."),
("What does FD_ISSET do?","Checks whether a descriptor remains marked ready after select returns."),
("What does man 2 select mean?","Manual section 2 is for system calls; it shows the Linux system-call interface, parameters, return values and errors."),
("Why is timeout called a maximum?","The call may return early when a descriptor becomes ready or due to interruption/error.")]),
("14. Determine file type","Medium","Take a path from the command line and identify any filesystem file type.",
"""Use <font name='Courier'>lstat(path,&s)</font> and inspect <font name='Courier'>s.st_mode</font> with macros such as S_ISREG, S_ISDIR, S_ISLNK, S_ISFIFO, S_ISSOCK, S_ISCHR, S_ISBLK.<br/>
lstat reports the path itself, so a symlink is recognized as a symlink. stat follows the final symlink. File type is determined from filesystem metadata, not from a filename extension.""",
[("Why lstat rather than stat?","To identify a symlink itself. stat would follow the final symlink."),
("What happens for a broken symlink?","lstat can still succeed and report a symlink; stat commonly fails because the target cannot be resolved."),
("Does the program open the file?","No; it obtains metadata with lstat.")]),
("15. environ","Medium","Display all environment variables using environ.",
"""<font name='Courier'>extern char **environ;</font> refers to the process environment array. Conceptually: environ → pointer to char* strings → \"NAME=value\" → ... → NULL.<br/>
Loop through pointers and print each string. The environment is normally supplied at process startup and inherited by children. <font name='Courier'>getenv</font> retrieves one variable; <font name='Courier'>setenv/unsetenv</font> modify the calling process's environment.""",
[("Why char **?","It is a pointer to an array of char pointers; each pointer points to a NAME=value string."),
("What ends the array?","A NULL pointer."),
("Is environ a system call?","No; it is a process environment interface/variable exposed by the C runtime."),
("Can a child change its parent's environment?","No. A child's environment is its own process state.")]),
("16. Mandatory locking","Hard","Implement read and write locking with fcntl; understand the mandatory/advisory distinction.",
"""<b>Critical viva point:</b> POSIX <font name='Courier'>fcntl</font> record locking is normally <i>advisory</i>. F_SETLKW means “set the lock and wait if it conflicts”; it does not by itself make the lock mandatory.<br/>
Traditional Linux mandatory locking historically required special filesystem/kernel conditions and file mode bits (classically setgid on + group execute off, e.g. 02660), and support/configuration is filesystem/version dependent. Therefore do not claim “fcntl automatically makes locking mandatory.”<br/>
F_RDLCK=shared read lock; F_WRLCK=exclusive write lock; F_UNLCK=unlock. l_whence/l_start/l_len define the byte range; l_len=0 means to EOF. F_SETLK is nonblocking; F_SETLKW waits.""",
[("Can multiple read locks coexist?","Yes, read locks can coexist when the ranges are compatible."),
("Can a write lock coexist with a read lock?","No; conflicting ranges block/conflict."),
("Is the lock on the filename?","No. It is a byte-range/record lock associated with the file/opening and process semantics."),
("What releases the lock?","Explicit unlock and the relevant close/process termination semantics release fcntl locks.")]),
("17. Online ticket reservation","Hard","Lock a ticket file, read the current number, increment it, and safely update it.",
"""Use an exclusive <font name='Courier'>F_WRLCK</font> with <font name='Courier'>F_SETLKW</font> so only one reservation process updates the number at a time. Seek to the beginning before reading and again before rewriting. Store the ticket as text (e.g. \"100\\n\"), parse it with atoi, increment, then write the new value. Truncate the file to the new length so stale old digits are not left behind.<br/>
<b>Race without lock:</b> A reads 100; B reads 100; both write 101. With lock: A gets 101, unlocks; B then reads 101 and writes 102.""",
[("Why write lock?","The operation modifies shared data, so it must exclude other readers/writers in the protected region."),
("Why lseek before reading/writing?","The file offset must be positioned at the desired location; after reading it may be at EOF."),
("Why ftruncate?","If the replacement value is shorter than the old content, it removes leftover bytes."),
("What does l_len=0 mean?","Lock from l_start through the end of the file."),
("What if the lock is removed?","Concurrent processes can read the same old value and generate duplicate ticket numbers.")]),
("18. Record locking","Hard","Create three records and lock only the record being accessed.",
"""With fixed-size records of 64 bytes: record 0 starts at 0, record 1 at 64, record 2 at 128. Set <font name='Courier'>l_start = r*SZ</font> and <font name='Courier'>l_len=SZ</font> to lock exactly one record.<br/>
Writer uses F_WRLCK; reader uses F_RDLCK. <font name='Courier'>pwrite/pread</font> access a specified offset without changing the process's current file offset. Different records can therefore be accessed concurrently; the same record conflicts appropriately.""",
[("Why is record locking better than whole-file locking here?","Independent records can proceed concurrently; only the record being accessed is protected."),
("Why pwrite/pread?","They specify the offset directly and do not alter the current file offset."),
("Can two readers access one record?","Yes, shared read locks can coexist."),
("Can a reader and writer access the same locked record simultaneously?","Not when their locks conflict.")]),
("19. Measure getpid with TSC","Hard","Estimate average time/cost of getpid using the CPU timestamp counter.",
"""Read the timestamp counter before and after N repeated calls: <font name='Courier'>end-start</font> is total TSC ticks observed; divide by N for an average per call. A large N amortizes measurement overhead/noise.<br/>
<font name='Courier'>__rdtsc()</font> is a compiler intrinsic, not a normal syscall. The result is cycles/ticks, not automatically nanoseconds. Modern glibc may cache/getpid in user space on some systems, so the benchmark measures the system's getpid interface as implemented, not necessarily a kernel transition on every iteration.""",
[("Why one million iterations?","To reduce the relative impact of loop/timestamp overhead and scheduling noise."),
("Why uint64_t?","The timestamp counter is a large nonnegative counter."),
("Is the result directly nanoseconds?","No. Converting cycles/ticks to time requires frequency information and careful benchmarking."),
("What adds measurement error?","Timestamp read overhead, loop overhead, scheduling/preemption, CPU migration/frequency behavior and lack of serialization.")]),
("20. Nice and process priority","Medium","Find the running program's nice value and modify it with the nice command.",
"""<font name='Courier'>getpriority(PRIO_PROCESS,0)</font> queries the calling process's nice value. On Linux, the usual nice range is -20 to +19: lower nice means higher preference under normal scheduling; higher nice means lower preference. The shell <font name='Courier'>nice -n 10 ./program</font> starts it with an adjusted niceness.<br/>
Changing nice is not the same as switching to SCHED_FIFO/RR. Ordinary users can generally make their own process less favored (increase nice); increasing priority by decreasing nice can require privilege.""",
[("Does nice guarantee CPU percentage?","No; scheduling also depends on runnable tasks, policy, CPUs and other factors."),
("Is nice the same as real-time priority?","No. Nice is associated with normal scheduling; FIFO/RR use real-time priority.")]),
("21. fork parent/child IDs","Easy","Call fork and print parent and child process IDs.",
"""<font name='Courier'>fork()</font> creates a child. Return value: -1 failure; 0 in child; child's PID in parent. Both continue from the instruction after fork.<br/>
Child can print getpid() and getppid(); parent can print its getpid() and the returned child PID. Output order is not guaranteed because the scheduler decides which process runs first. Modern fork uses copy-on-write for memory pages.""",
[("Why different return values?","So parent and child can determine which execution path they are in."),
("Can child output appear first?","Yes. Scheduling is not guaranteed."),
("What does getppid return?","The current parent PID.")]),
("22. Open before fork, then both write","Hard","Open a file, fork, and have parent and child write to it.",
"""Because the file is opened <i>before</i> fork, the inherited FDs in parent and child refer to the same open file description. That means they share the current file offset and status flags.<br/>
If child writes first, parent writes after its data; if parent writes first, order reverses. <font name='Courier'>wait()</font> after the parent's write does not force child-first; it only makes the parent wait after it has already written. If each process opened the file separately after fork, their open file descriptions would generally be separate.""",
[("Why is FD number the same in both processes?","Each process has its own FD table, so the same integer can refer to the inherited shared open file description."),
("Why is output order unpredictable?","The scheduler decides which process executes its write first."),
("What does close do?","It closes that process's descriptor; the shared open state remains while other references exist.")]),
("23. Zombie process","Medium","Create a child that exits while the parent remains alive without waiting.",
"""A zombie is a terminated child whose parent has not yet collected its termination status. The kernel retains small bookkeeping such as PID and exit status. The child is not executing.<br/>
The demo parent sleeps, allowing <font name='Courier'>ps</font> to show state Z/<defunct>. A later wait/waitpid reaps it. This is different from an orphan: an orphan is still running after its parent dies.""",
[("How is zombie different from orphan?","Zombie: child died first, parent alive and hasn't reaped it. Orphan: parent died first, child still runs."),
("Why _exit?","It terminates immediately without stdio/atexit cleanup; useful after fork in a child when appropriate."),
("How is zombie removed?","The parent calls wait/waitpid, or reparenting allows a suitable system process to reap it.")]),
("24. Orphan process","Easy","Create a child that remains alive after the parent exits.",
"""Parent calls fork and exits immediately. Child sleeps so the parent has time to terminate. The child then prints getpid and getppid. Because its original parent is gone, it is reparented/adopted by PID 1 or an appropriate configured subreaper.""",
[("Does the child die when parent exits?","No; it continues running."),
("Is an orphan a zombie?","No. The orphan is still executing; a zombie has already terminated."),
("Why sleep?","To ensure the parent exits before the child prints its new PPID.")]),
("25. Three children and waitpid","Medium","Create three children and wait specifically for child 2.",
"""Store each child PID in c[0..2]. Each child prints its PID, sleeps for a different time, then exits with a different status. Parent calls <font name='Courier'>waitpid(c[1],&st,0)</font>, which blocks specifically for child 2. WIFEXITED checks normal termination; WEXITSTATUS extracts its exit code. Parent then waits for the other children to prevent leftover zombies.""",
[("What if child 1 finishes first?","Parent remains blocked waiting specifically for child 2. Child 1 can temporarily be a zombie until reaped later."),
("wait vs waitpid?","wait generally waits for any child; waitpid can select a specific PID (or other selection modes)."),
("Why store PIDs?","The parent needs the exact PID to wait for a particular child.")]),
("26. Execute an executable with exec","Medium","Execute another executable and pass command-line input.",
"""<font name='Courier'>exec</font> replaces the current process image; it does not create a new process and normally keeps the same PID. Example: <font name='Courier'>execl(\"/bin/echo\",\"echo\",name,NULL)</font>.<br/>
If exec succeeds, it never returns, so code after it executes only on failure. <font name='Courier'>perror</font> is therefore placed after exec. argv[0] conventionally names the program; subsequent entries are its arguments.""",
[("fork vs exec?","fork creates a new process; exec replaces the current program."),
("Why NULL?","It terminates the variadic argument list for l-style exec calls."),
("What if execl fails?","It returns -1, errno is set, and perror can report the reason.")]),
("27. execl/execlp/execle/execv/execvp","Hard","Execute ls -Rl using all five exec variants.",
"""All five execute the same program; they differ in argument representation, PATH search and environment.<br/>
<font name='Courier'>l</font>=list arguments; <font name='Courier'>v</font>=vector/array; <font name='Courier'>p</font>=search PATH; <font name='Courier'>e</font>=explicit environment.<br/>
execl: explicit path + list. execlp: PATH + list. execle: explicit path + list + supplied environment. execv: explicit path + array. execvp: PATH + array.""",
[("What does -R mean?","Recursive listing."),
("What does -l mean?","Long listing format."),
("Why use execvp(\"ls\",a)?","It supplies arguments as an array and lets the system search PATH for ls."),
("Does any of these create a process?","No; exec replaces the current process image.")]),
("28. Get min/max real-time priority","Medium","Get minimum and maximum real-time priorities for SCHED_FIFO and SCHED_RR.",
"""<font name='Courier'>sched_get_priority_min(policy)</font> and <font name='Courier'>sched_get_priority_max(policy)</font> query the valid priority range for a scheduling policy. SCHED_FIFO and SCHED_RR are real-time policies. Exact numeric ranges should be obtained from the system rather than assumed.<br/>
This program only queries; it does not change the process policy or priority.""",
[("FIFO vs RR?","FIFO does not time-slice equal-priority runnable threads merely because a quantum expires; RR rotates equal-priority threads using a time quantum."),
("Does this change priority?","No, it only reads the supported range."),
("Is real-time priority the same as nice?","No; they belong to different scheduling mechanisms.")]),
("29. Get and modify scheduling policy","Hard","Read the current policy and change it to SCHED_FIFO or SCHED_RR.",
"""<font name='Courier'>sched_getscheduler(0)</font> gets the calling process's current policy. <font name='Courier'>sched_setscheduler(0,target,&sp)</font> changes the policy and scheduling parameters. For FIFO/RR, <font name='Courier'>struct sched_param</font> contains a valid real-time priority; this example uses the minimum for the target policy.<br/>
Changing to a real-time policy may require appropriate privileges/capabilities; failure is commonly EPERM for an unprivileged attempt.""",
[("What does 0 mean?","The calling process."),
("What is SCHED_OTHER?","The normal/default scheduling policy on typical Linux systems."),
("What is the difference from Q28?","Q28 queries valid priority bounds; Q29 queries the current policy and attempts to change the policy."),
("Does sched_getscheduler change anything?","No; it only queries.")]),
("30. Run a script at a specific time with a daemon","Hard","Daemonize a process, check local time, and execute a shell script at a specified HH:MM.",
"""<b>Flow:</b> validate HH:MM → fork → parent exits → child calls setsid → chdir(\"/\") → umask(0) → redirect 0/1/2 to /dev/null → repeatedly call time/localtime_r → when hour/minute match, fork → child execl(\"/bin/sh\",\"sh\",script,NULL) → daemon waitpid → sleep to avoid duplicate execution.<br/>
<font name='Courier'>setsid()</font> creates a new session and detaches from the old controlling terminal/session. chdir(\"/\") avoids holding an arbitrary working directory. /dev/null prevents terminal dependency. The second fork is the script child; exec replaces it with the shell script.""",
[("Why waitpid after launching the script?","To reap the script child and avoid leaving a zombie."),
("Why sleep 61 after a match?","To prevent repeated executions during the same matching minute."),
("Is this a production scheduler?","No; it demonstrates daemonization/scheduling concepts. Production daemons usually add logging, signal handling, robust lifecycle/error handling, privilege management, etc."),
("Why use cron in real life?","cron is an existing scheduling service designed for this job; the lab is demonstrating how a simple scheduler/daemon can be implemented.")])
]

# Added 'explanation' to match the 5 elements in each tuple
for i, (titletext, diff, desc, explanation, qs) in enumerate(questions):
    story.append(PageBreak() if i else Spacer(1, 10))
    story.append(P("Q" + str(i + 1) + " — " + titletext, h1))
    
    # You can now use the 'explanation' variable inside your story building!
    story.append(P(explanation, body)) 

    t=Table([[P("<b>Difficulty</b>",difficulty),P("<b>Viva target</b>",difficulty)],
             [P(diff,difficulty),P("Explain flow + OS concept + follow-ups",difficulty)]], colWidths=[45*mm,125*mm])
    t.setStyle(TableStyle([("GRID",(0,0),(-1,-1),0.5,colors.grey),("VALIGN",(0,0),(-1,-1),"MIDDLE"),("BACKGROUND",(0,0),(-1,0),colors.whitesmoke)]))
    story += [t,Spacer(1,6),P("<b>Question:</b> "+titletext+" — "+desc,body)]
    for q,a in qs:
        story += Q(q,a)
    # add quick answer structure
    story += [P("<b>Viva answer structure:</b> Start with the purpose → show the execution flow → explain the important call/parameters → explain what the kernel/OS is doing → mention one edge case or “what if?”",small)]

story += [PageBreak(),P("LAST-MINUTE LINUX + OS BASICS",h1)]
basics=[
("What is a process?","A running program plus its execution state/resources: PID, address space, registers/context, open FDs, scheduling information, credentials, etc."),
("Program vs process","A program is passive code/data on storage. A process is a running instance of that program."),
("Kernel","The privileged core of the OS that manages CPU, memory, filesystems, devices, processes and provides system-call interfaces."),
("System call","A controlled interface through which user programs request kernel services, e.g. open, read, write, fork, exec, waitpid."),
("Library function vs system call","A library function is a user-space API; it may call a system call, wrap it, or do work entirely in user space. Example: printf is stdio; write is a system-call interface."),
("User mode vs kernel mode","User programs normally run with restricted privileges; kernel mode has the privileges needed to manage protected OS resources."),
("File descriptor","A small integer in a process's FD table referring to an open resource. 0/1/2 are stdin/stdout/stderr."),
("Inode","Filesystem metadata object identifying a file and containing metadata; directory entries map names to inode objects."),
("Directory entry","The filesystem's mapping from a filename to an inode/object; a filename is not the file's data itself."),
("Open file description","Kernel-side state created by open, including current file offset and status flags; duplicated FDs can share it."),
("Buffering","stdio may buffer output/input. stdout is commonly line-buffered on a terminal and fully buffered when redirected; stderr is typically unbuffered."),
("errno/perror","A failed system/library interface commonly returns an error indicator and sets errno. perror prints a prefix plus a readable errno message."),
("fork/exec/wait","fork creates a child; exec replaces a process image; wait/waitpid collects child termination status and prevents zombies."),
("Zombie vs orphan","Zombie = terminated child not reaped. Orphan = still-running child whose parent terminated."),
("PPID/PID","PID identifies a process; PPID identifies its current parent."),
("Pipe vs FIFO","An anonymous pipe is commonly used between related processes; a FIFO is a named pipe represented in the filesystem and can be opened by unrelated processes."),
("Hard link vs symlink","Hard link shares inode; symlink stores a pathname/reference."),
("Blocking","A blocking call may wait until an operation can proceed. select can wait for readiness; read may block until data/EOF depending on object."),
("Readiness vs data","select says an operation can proceed without blocking; it does not itself consume data."),
("Permissions vs access mode","open's O_RDONLY/O_WRONLY/O_RDWR controls how that open is used; filesystem mode bits such as 0644 control permission checks."),
("Race condition","Result depends on timing/interleaving of concurrent operations. Locking protects critical sections."),
("Advisory vs mandatory locking","Advisory locks work when cooperating programs honor them. Traditional mandatory locking requires specific OS/filesystem conditions and is not automatic just because fcntl is used."),
("Scheduling","The scheduler decides which runnable thread/process gets CPU time. Normal scheduling and real-time FIFO/RR use different mechanisms."),
("Nice vs real-time priority","Nice adjusts relative preference under normal scheduling; SCHED_FIFO/RR use real-time priorities."),
("Daemon","A long-running background service designed to operate independently of an interactive terminal/session."),
("PATH","A colon-separated list of directories searched by PATH-aware exec functions such as execlp/execvp."),
("stdin/stdout/stderr redirection","Shell redirection changes where standard descriptors point, e.g. > for stdout and 2> for stderr."),
]
data=[]
for name,ans in basics:
    data.append([P("<b>"+name+"</b>",small),P(ans,small)])
tb=Table(data,colWidths=[48*mm,122*mm],repeatRows=0)
tb.setStyle(TableStyle([("GRID",(0,0),(-1,-1),0.35,colors.lightgrey),("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),5),("RIGHTPADDING",(0,0),(-1,-1),5),("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4)]))
story.append(tb)
story += [Spacer(1,8),P("<b>Random-question viva drill:</b> Pick any Q1–Q30. Explain it aloud without reading for 60–90 seconds. Then answer: Why this call? What does each important parameter mean? What happens if it fails? What happens if two processes do it simultaneously? What changes if I remove/replace this call? Where is the relevant information stored (user space/kernel/filesystem)?",body),
          P("<b>Important:</b> The difficulty labels are a study-planning aid, not official TA ratings. The lab sheet itself specifies the 30 questions; this guide expands them with the concepts and follow-ups needed to explain them.",small)]

def footer(canvas,doc):
    canvas.saveState()
    canvas.setFont("Helvetica",7.5)
    canvas.drawString(15*mm,8*mm,"System Software Viva — 30 Questions")
    canvas.drawRightString(A4[0]-15*mm,8*mm,f"Page {doc.page}")
    canvas.restoreState()

doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(out)
