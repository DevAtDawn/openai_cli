file=$1
text=$(cat $file)
# echo $text $file 
prompt=$(cat $file | head -n-1)
instruction=$(cat $file | tail -n1)
# echo $prompt $instruction
openai_cli "${prompt}" "${instruction}"
