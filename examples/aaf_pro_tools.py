import aaf2
import argparse
import os.path


def make_aaf(sequence_name, timeline_fps = 24, sample_rate = 48000, output_file='TestForImport.aaf', link_files = []):

    with aaf2.open(output_file, 'w') as f:
        master_mobs = []

        for filename in link_files:
            metadata = probe(filename)
            mobs = aaf2.ama.create_wav_link(f, metadata)
            master_mobs.append(mobs[0])

        # for filename in embed_files:
        #     master_mob = f.create.MasterMob()
        #     master_mob.import_audio_essence(path=filename, edit_rate=sample_rate)
        #     master_mobs.append(master_mob)

        comp_mob = f.create.CompositionMob()
        f.content.mobs.append(comp_mob)
        comp_mob.name = sequence_name
        comp_mob.usage = 'Usage_TopLevel'

        timecode_slot = comp_mob.create_empty_sequence_slot(timeline_fps,
                                                            media_kind='Timecode')
        timecode_component = f.create.Timecode(timeline_fps, drop=False)
        timecode_component.start = 0
        timecode_component.length = timeline_fps * 60 * 60 * 12

        timecode_slot.segment.components.append(timecode_component)
        timecode_slot.name = 'TC1'

        track_1_slot = comp_mob.create_sound_slot(sample_rate)
        track_1_slot.name = "Audio 1"

        for master_mob in master_mobs:
            clip = master_mob.create_source_clip(master_mob.slots[0].slot_id, start=0)
            track_1_slot.segment.components.append(clip)


arg_parser = argparse.ArgumentParser(description="Demonstrate a minimal AAF that can be opened by Avid Pro Tools.")
arg_parser.add_argument('-n', '--name', help='Set the name of the composition.', default='Demo Composition')
arg_parser.add_argument('--fps', help='Set the integer frame rate of the timecode ruler.', default=24)
arg_parser.add_argument('-r', '--rate', help='Set the sample rate for the session.', default=48000)

arg_parser.add_argument('--link', help='Add a source sound file by AMA linking.',  action='append')
#arg_parser.add_argument('--embed', help="Add a source sound file by embedding.", action='append')
arg_parser.add_argument('outputfile', metavar='OUTPUT.aaf', help='Set the name of the output AAF file.',
                        default='output.aaf', nargs='?')
args = arg_parser.parse_args()
print(args)