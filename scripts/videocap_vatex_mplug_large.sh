#sh videocap_vatex_mplug_large.sh
#pip install colorlog
#apt-get update
#apt-get install default-jdk
#apt-get install default-jre
#pip install git+git://github.com/j-min/language-evaluation@master
#python -c "import language_evaluation; language_evaluation.download('coco')"
#--config configs/videocap_vatext_mplug_large.yaml \

python videocap_mplug.py --output_dir output/videocap_creative_mplug_explanation_new \
    --checkpoint mplug_large.pth \
    --do_two_optim \
    --min_length 15 \
    --beam_size 10 \
    --max_length 25 \
    --max_input_length 25 \
    --evaluate
