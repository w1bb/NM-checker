function run_test()
    source('./task-1.m')
    fout = fopen('out', 'w+');
    A = implemented_by_student_ok()
    for i=1:size(A, 1)
        fprintf(fout, '%f ', A(i,:));
        fprintf(fout, '\n');
    end
    fclose(fout);
end