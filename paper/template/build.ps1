$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
New-Item -ItemType Directory -Force -Path review | Out-Null
& 'D:\ana\python.exe' scripts/build_assets.py
if ($LASTEXITCODE -ne 0) { throw 'Plot generation failed' }
& 'D:\ana\python.exe' scripts/build_references.py
if ($LASTEXITCODE -ne 0) { throw 'Bibliography generation failed' }
& 'D:\ana\python.exe' scripts/build_capabilities.py
if ($LASTEXITCODE -ne 0) { throw 'Capability table failed' }
& 'D:\ana\python.exe' scripts/build_revision.py
if ($LASTEXITCODE -ne 0) { throw 'Revision plots failed' }
& 'D:\ana\python.exe' scripts/intake_route.py
if ($LASTEXITCODE -ne 0) { throw 'Route intake failed' }
& 'D:\ana\python.exe' scripts/verify_matched.py
if ($LASTEXITCODE -ne 0) { throw 'Matched RTL audit failed' }
& 'D:\ana\python.exe' scripts/intake_gpu.py
if ($LASTEXITCODE -ne 0) { throw 'GPU intake failed' }
& 'D:\ana\python.exe' scripts/revise_manuscript.py
if ($LASTEXITCODE -ne 0) { throw 'Manuscript revision failed' }
& 'D:\ana\python.exe' scripts/finalize_visuals.py
if ($LASTEXITCODE -ne 0) { throw 'Corrected visual artwork failed' }
pdflatex -interaction=nonstopmode -halt-on-error main.tex | Out-File -Encoding utf8 review/latex_pass1.txt
if ($LASTEXITCODE -ne 0) { throw 'LaTeX pass 1 failed' }
bibtex main | Out-File -Encoding utf8 review/bibtex.txt
if ($LASTEXITCODE -ne 0) { throw 'BibTeX failed' }
pdflatex -interaction=nonstopmode -halt-on-error main.tex | Out-File -Encoding utf8 review/latex_pass2.txt
if ($LASTEXITCODE -ne 0) { throw 'LaTeX pass 2 failed' }
pdflatex -interaction=nonstopmode -halt-on-error main.tex | Out-File -Encoding utf8 review/latex_pass3.txt
if ($LASTEXITCODE -ne 0) { throw 'LaTeX pass 3 failed' }
& 'D:\ana\python.exe' scripts/check_paper.py
if ($LASTEXITCODE -ne 0) { throw 'Artifact check failed' }
